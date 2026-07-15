import SwiftSyntax
import SwiftSyntaxBuilder
import SwiftSyntaxMacros

/**
 Member macro applied to a `Record` type. Scans the body for `@Field`-annotated
 stored properties and synthesizes `_recordFields(of:)`, returning each field
 paired with its compile-time key. This replaces the runtime `Mirror` walk in
 `fieldsOf(_:)` and lets the framework drop the lazy keying that today protects
 the field's options with a `Mutex`.

   @Record
   struct Options: Record {
     @Field var name: String = ""
     @Field(.required) var count: Int = 0
     @Field(.keyed("custom_key")) var flag: Bool = false
   }

 Expansion:

   public static func _recordFields(of instance: Self) -> [RecordFieldDescriptor] {
     var fields: [RecordFieldDescriptor] = []
     fields.append(RecordFieldDescriptor(key: "name",       isRequired: false, field: instance._name))
     fields.append(RecordFieldDescriptor(key: "count",      isRequired: true,  field: instance._count))
     fields.append(RecordFieldDescriptor(key: "custom_key", isRequired: false, field: instance._flag))
     return fields
   }

 `isRequired` is computed from the `@Field` attribute arguments at compile time so the
 framework can avoid a `Mutex.withLock` per field per call.

 For classes that inherit from another `@Record`-annotated class, the macro
 prepends `super._recordFields(of: instance)` so inherited fields appear first.
 */
public struct RecordMacro: MemberMacro, ExtensionMacro {
  public static func expansion(
    of node: AttributeSyntax,
    providingMembersOf declaration: some DeclGroupSyntax,
    conformingTo protocols: [TypeSyntax],
    in context: some MacroExpansionContext
  ) throws -> [DeclSyntax] {
    let isClass = declaration.is(ClassDeclSyntax.self)
    guard declaration.is(StructDeclSyntax.self) || isClass else {
      throw MacroExpansionErrorMessage("@Record can only be applied to a struct or class")
    }

    var entries: [(propertyName: String, key: String, isRequired: Bool)] = []

    for member in declaration.memberBlock.members {
      guard let varDecl = member.decl.as(VariableDeclSyntax.self),
        let attribute = varDecl.attributes.firstAttribute(named: "Field") else {
        continue
      }
      for binding in varDecl.bindings {
        guard let ident = binding.pattern.as(IdentifierPatternSyntax.self) else {
          continue
        }
        let propertyName = ident.identifier.text
        let key = explicitKeyArgument(of: attribute) ?? propertyName
        let isRequired = hasRequiredArgument(of: attribute)
        entries.append((propertyName, key, isRequired))
      }
    }

    let inheritsRecord = isClass && classHasInheritance(declaration)
    let overrideKeyword = inheritsRecord ? "override " : ""

    var lines: [String] = []
    if inheritsRecord {
      lines.append("  var fields: [RecordFieldDescriptor] = super._recordFields(of: instance)")
    } else {
      lines.append("  var fields: [RecordFieldDescriptor] = []")
    }
    for entry in entries {
      let requiredLiteral = entry.isRequired ? "true" : "false"
      lines.append("  fields.append(RecordFieldDescriptor(key: \"\(entry.key)\", isRequired: \(requiredLiteral), field: instance._\(entry.propertyName)))")
    }
    lines.append("  return fields")

    let body = lines.joined(separator: "\n")

    let method: DeclSyntax = """
      public \(raw: overrideKeyword)class func _recordFields(of instance: Self) -> [RecordFieldDescriptor] {
      \(raw: body)
      }
      """

    let staticMethod: DeclSyntax = """
      public static func _recordFields(of instance: Self) -> [RecordFieldDescriptor] {
      \(raw: body)
      }
      """

    return [isClass ? method : staticMethod]
  }

  /**
   Adds `Record` and `_RecordFieldsProvider` conformances. Each is only added when the type
   doesn't already declare it — Swift rejects redundant conformances, so the macro must check
   the inheritance clause syntactically.

   For class subclasses (which inherit conformance from a `@Record`-annotated parent), no
   extension is emitted at all. The user can write either `@Record struct Options { ... }`
   or `@Record struct Options: Record { ... }`; both work.
   */
  public static func expansion(
    of node: AttributeSyntax,
    attachedTo declaration: some DeclGroupSyntax,
    providingExtensionsOf type: some TypeSyntaxProtocol,
    conformingTo protocols: [TypeSyntax],
    in context: some MacroExpansionContext
  ) throws -> [ExtensionDeclSyntax] {
    if declaration.is(ClassDeclSyntax.self) && classHasInheritance(declaration) {
      return []
    }
    guard declaration.is(StructDeclSyntax.self) || declaration.is(ClassDeclSyntax.self) else {
      return []
    }

    var conformances: [String] = []
    if !inheritsProtocol(named: "Record", in: declaration) {
      conformances.append("Record")
    }
    if !inheritsProtocol(named: "_RecordFieldsProvider", in: declaration) {
      conformances.append("_RecordFieldsProvider")
    }
    if conformances.isEmpty {
      return []
    }

    let ext: DeclSyntax = """
      extension \(type.trimmed): \(raw: conformances.joined(separator: ", ")) {}
      """
    guard let extDecl = ext.as(ExtensionDeclSyntax.self) else {
      return []
    }
    return [extDecl]
  }
}

/**
 True if the type's inheritance clause already lists a protocol with the given name.
 Matches either the bare identifier (`Record`) or a qualified member access ending in
 the name (`ExpoModulesCore.Record`). Typealiases can't be resolved syntactically, so a
 user who refers to `Record` via a typealias will get a redundant-conformance error from
 the macro-emitted extension and should drop the alias for the inheritance clause.
 */
private func inheritsProtocol(named name: String, in declaration: some DeclGroupSyntax) -> Bool {
  let inheritanceClause: InheritanceClauseSyntax?
  if let structDecl = declaration.as(StructDeclSyntax.self) {
    inheritanceClause = structDecl.inheritanceClause
  } else if let classDecl = declaration.as(ClassDeclSyntax.self) {
    inheritanceClause = classDecl.inheritanceClause
  } else {
    return false
  }
  guard let inherited = inheritanceClause?.inheritedTypes else {
    return false
  }
  for entry in inherited {
    let typeSyntax = entry.type
    if let identifier = typeSyntax.as(IdentifierTypeSyntax.self),
      identifier.name.text == name {
      return true
    }
    if let member = typeSyntax.as(MemberTypeSyntax.self),
      member.name.text == name {
      return true
    }
  }
  return false
}

/**
 True if the class declaration has any inheritance clause. Used as a heuristic for
 whether the superclass also conforms to `Record` and provides `_recordFields(of:)`.
 The macro emits an `override` in this case; if the superclass is not a `Record`,
 the user gets a clear compiler error pointing at the missing override target.
 */
private func classHasInheritance(_ declaration: some DeclGroupSyntax) -> Bool {
  guard let classDecl = declaration.as(ClassDeclSyntax.self),
    let inherited = classDecl.inheritanceClause?.inheritedTypes,
    !inherited.isEmpty else {
    return false
  }
  return true
}

/**
 True if the `@Field` attribute has `.required` as one of its arguments. The check is purely
 syntactic — it matches the literal member-access expression `.required`. Variants like
 `FieldOption.required` or aliased identifiers won't be detected; the framework still falls
 back to the field's runtime `isRequired` for correctness in those cases (see `Record.swift`).
 */
private func hasRequiredArgument(of attribute: AttributeSyntax) -> Bool {
  guard let args = attribute.arguments?.as(LabeledExprListSyntax.self) else {
    return false
  }
  for arg in args {
    if let member = arg.expression.as(MemberAccessExprSyntax.self),
      member.declName.baseName.text == "required" {
      return true
    }
  }
  return false
}

/**
 Extracts the dictionary key from a `@Field` attribute. Recognizes both forms:
 a bare string literal (`@Field("custom_key")`, relying on
 `FieldOption: ExpressibleByStringLiteral`) and the explicit factory call
 (`@Field(.keyed("custom_key"))`). Returns nil if neither is present; other
 `FieldOption` cases (`.required`, etc.) are ignored.
 */
private func explicitKeyArgument(of attribute: AttributeSyntax) -> String? {
  guard let args = attribute.arguments?.as(LabeledExprListSyntax.self) else {
    return nil
  }
  for arg in args {
    if let str = arg.expression.as(StringLiteralExprSyntax.self),
      let segment = str.segments.first?.as(StringSegmentSyntax.self) {
      return segment.content.text
    }
    if let call = arg.expression.as(FunctionCallExprSyntax.self),
      let member = call.calledExpression.as(MemberAccessExprSyntax.self),
      member.declName.baseName.text == "keyed",
      let firstArg = call.arguments.first,
      let str = firstArg.expression.as(StringLiteralExprSyntax.self),
      let segment = str.segments.first?.as(StringSegmentSyntax.self) {
      return segment.content.text
    }
  }
  return nil
}
