import SwiftSyntax
import SwiftSyntaxBuilder
import SwiftSyntaxMacros

/**
 Member macro applied to a `Module` subclass. Scans the class body for declarations
 marked with `@JS` and synthesizes a framework-internal `_exposedDefinition()`
 method returning `[AnyDefinition]`. `expo-modules-core` calls it automatically
 and merges the result into the module's definition.

   @ExpoModule
   public final class MyModule: Module {
     public func definition() -> ModuleDefinition {
       Name("MyModule")
     }

     @JS
     func greet(name: String) -> String { "Hi, \(name)" }
   }
 */
public struct ExpoModuleMacro: MemberMacro {
  public static func expansion(
    of node: AttributeSyntax,
    providingMembersOf declaration: some DeclGroupSyntax,
    conformingTo protocols: [TypeSyntax],
    in context: some MacroExpansionContext
  ) throws -> [DeclSyntax] {
    guard let classDecl = declaration.as(ClassDeclSyntax.self) else {
      throw MacroExpansionErrorMessage("@ExpoModule can only be applied to a class")
    }

    let moduleName = jsNameArgument(of: node) ?? classDecl.name.text
    var entries: [String] = ["Name(\"\(moduleName)\")"]

    for typeName in classListArgument(of: node, label: "classes") {
      entries.append("\(typeName)._exposedClassDefinition()")
    }

    for member in classDecl.memberBlock.members {
      let decl = member.decl

      if let funcDecl = decl.as(FunctionDeclSyntax.self),
        let attribute = funcDecl.attributes.firstAttribute(named: "JS") {
        entries.append(buildFunctionEntry(funcDecl: funcDecl, attribute: attribute))
        continue
      }

      if let varDecl = decl.as(VariableDeclSyntax.self),
        let attribute = varDecl.attributes.firstAttribute(named: "JS") {
        entries.append(contentsOf: buildPropertyEntries(varDecl: varDecl, attribute: attribute))
      }
    }

    let lines = entries.map { "    \($0)" }.joined(separator: ",\n")
    let body = "  return [\n\(lines)\n  ]"

    let method: DeclSyntax = """
      public func _exposedDefinition() -> [AnyDefinition] {
      \(raw: body)
      }
      """

    return [method]
  }
}

// MARK: - Member builders

private func buildFunctionEntry(
  funcDecl: FunctionDeclSyntax,
  attribute: AttributeSyntax
) -> String {
  let swiftName = funcDecl.name.text
  let jsName = jsNameArgument(of: attribute) ?? swiftName
  let isAsync = funcDecl.signature.effectSpecifiers?.asyncSpecifier != nil
  let dslEntry = isAsync ? "AsyncFunction" : "Function"
  return "\(dslEntry)(\"\(jsName)\", \(swiftName))"
}

private func buildPropertyEntries(
  varDecl: VariableDeclSyntax,
  attribute: AttributeSyntax
) -> [String] {
  let jsNameOverride = jsNameArgument(of: attribute)

  return varDecl.bindings.compactMap { binding in
    guard let ident = binding.pattern.as(IdentifierPatternSyntax.self) else {
      return nil
    }
    let swiftName = ident.identifier.text
    let jsName = jsNameOverride ?? swiftName
    return "Property(\"\(jsName)\") { self.\(swiftName) }"
  }
}

