import SwiftSyntax
import SwiftSyntaxBuilder
import SwiftSyntaxMacros

/**
 Member macro applied to a `SharedObject` subclass. Scans the class body for
 declarations marked with `@JS` and synthesizes `_exposedClassDefinition()`,
 returning a `ClassDefinition` ready to drop into a module's `Class { ... }` slot.

   @SharedObject
   final class Cache: SharedObject {
     @JS
     init(name: String) { self.name = name }

     @JS
     func get(_ key: String) -> String? { ... }

     @JS
     var size: Int { 42 }
   }

 The companion `@ExpoModule(classes: [Cache.self])` wires the resulting
 definition into the module's exposed surface.
 */
public struct SharedObjectMacro: MemberMacro {
  public static func expansion(
    of node: AttributeSyntax,
    providingMembersOf declaration: some DeclGroupSyntax,
    conformingTo protocols: [TypeSyntax],
    in context: some MacroExpansionContext
  ) throws -> [DeclSyntax] {
    guard let classDecl = declaration.as(ClassDeclSyntax.self) else {
      throw MacroExpansionErrorMessage("@SharedObject can only be applied to a class")
    }

    guard inheritsFromSharedObject(classDecl) else {
      throw MacroExpansionErrorMessage(
        "@SharedObject class must inherit from SharedObject. Add `: SharedObject` to the class declaration.")
    }

    let typeName = classDecl.name.text
    let jsName = jsNameArgument(of: node) ?? typeName

    var entries: [String] = []
    var sawConstructor = false

    for member in classDecl.memberBlock.members {
      let decl = member.decl

      if let initDecl = decl.as(InitializerDeclSyntax.self),
        initDecl.attributes.firstAttribute(named: "JS") != nil {
        if sawConstructor {
          throw MacroExpansionErrorMessage(
            "@SharedObject classes can have at most one @JS initializer; JavaScript classes have a single constructor.")
        }
        sawConstructor = true
        entries.append(buildConstructorEntry(initDecl: initDecl, typeName: typeName))
        continue
      }

      if let funcDecl = decl.as(FunctionDeclSyntax.self),
        let attribute = funcDecl.attributes.firstAttribute(named: "JS") {
        entries.append(
          buildClassFunctionEntry(funcDecl: funcDecl, attribute: attribute, typeName: typeName))
        continue
      }

      if let varDecl = decl.as(VariableDeclSyntax.self),
        let attribute = varDecl.attributes.firstAttribute(named: "JS") {
        entries.append(
          contentsOf: buildClassPropertyEntries(
            varDecl: varDecl, attribute: attribute, typeName: typeName))
      }
    }

    let lines = entries.map { "    \($0)" }.joined(separator: "\n")
    let body = entries.isEmpty
      ? "  return Class(\"\(jsName)\", \(typeName).self) {\n  }"
      : "  return Class(\"\(jsName)\", \(typeName).self) {\n\(lines)\n  }"

    let method: DeclSyntax = """
      public static func _exposedClassDefinition() -> ClassDefinition {
      \(raw: body)
      }
      """

    return [method]
  }
}

// MARK: - Inheritance check

private func inheritsFromSharedObject(_ classDecl: ClassDeclSyntax) -> Bool {
  guard let inherited = classDecl.inheritanceClause?.inheritedTypes else {
    return false
  }
  for entry in inherited {
    if baseIdentifier(of: entry.type) == "SharedObject" {
      return true
    }
  }
  return false
}

private func baseIdentifier(of type: TypeSyntax) -> String? {
  if let identifier = type.as(IdentifierTypeSyntax.self) {
    return identifier.name.text
  }
  if let member = type.as(MemberTypeSyntax.self) {
    return member.name.text
  }
  return nil
}

// MARK: - Class-scope entry builders

private func buildClassFunctionEntry(
  funcDecl: FunctionDeclSyntax,
  attribute: AttributeSyntax,
  typeName: String
) -> String {
  let swiftName = funcDecl.name.text
  let jsName = jsNameArgument(of: attribute) ?? swiftName
  let effects = funcDecl.signature.effectSpecifiers
  let isAsync = effects?.asyncSpecifier != nil
  let isThrowing = effects?.throwsClause?.throwsSpecifier != nil
  let dslEntry = isAsync ? "AsyncFunction" : "Function"

  let params = funcDecl.signature.parameterClause.parameters
  let closureParamList: String
  let callArgList: String
  if params.isEmpty {
    closureParamList = "(this: \(typeName))"
    callArgList = ""
  } else {
    let typedParams = params.enumerated().map { index, param in
      "_ arg\(index): \(param.type.trimmedDescription)"
    }.joined(separator: ", ")
    closureParamList = "(this: \(typeName), \(typedParams))"

    callArgList = params.enumerated().map { index, param in
      let label = param.firstName.text
      return label == "_" ? "arg\(index)" : "\(label): arg\(index)"
    }.joined(separator: ", ")
  }

  let awaitKeyword = isAsync ? "await " : ""
  let tryKeyword = (isAsync || isThrowing) ? "try " : ""
  let callExpr = "\(tryKeyword)\(awaitKeyword)this.\(swiftName)(\(callArgList))"

  return "\(dslEntry)(\"\(jsName)\") { \(closureParamList) in \(callExpr) }"
}

private func buildClassPropertyEntries(
  varDecl: VariableDeclSyntax,
  attribute: AttributeSyntax,
  typeName: String
) -> [String] {
  let jsNameOverride = jsNameArgument(of: attribute)

  return varDecl.bindings.compactMap { binding in
    guard let ident = binding.pattern.as(IdentifierPatternSyntax.self) else {
      return nil
    }
    let swiftName = ident.identifier.text
    let jsName = jsNameOverride ?? swiftName
    return "Property(\"\(jsName)\") { (this: \(typeName)) in this.\(swiftName) }"
  }
}

private func buildConstructorEntry(
  initDecl: InitializerDeclSyntax,
  typeName: String
) -> String {
  let params = initDecl.signature.parameterClause.parameters

  if params.isEmpty {
    return "Constructor { \(typeName)() }"
  }

  let argList = params.enumerated().map { index, param in
    "_ arg\(index): \(param.type.trimmedDescription)"
  }.joined(separator: ", ")

  let callArgs = params.enumerated().map { index, param in
    let label = param.firstName.text
    return label == "_" ? "arg\(index)" : "\(label): arg\(index)"
  }.joined(separator: ", ")

  return "Constructor { (\(argList)) in \(typeName)(\(callArgs)) }"
}
