import SwiftSyntax
import SwiftSyntaxMacros

/**
 Marker macro applied to module / shared-object members that should be exposed to JavaScript.
 Expands to nothing on its own; `@ExpoModule` and `@SharedObject` discover declarations
 carrying this attribute and generate the corresponding `Function` / `AsyncFunction` /
 `Property` / `Constructor` registrations.

 Usage:

   @JS
   func greet(name: String) -> String { ... }

   @JS("doWork")
   func performWork() async throws { ... }

   @JS
   var status: String { "ok" }
 */
public struct JSMacro: PeerMacro {
  public static func expansion(
    of node: AttributeSyntax,
    providingPeersOf declaration: some DeclSyntaxProtocol,
    in context: some MacroExpansionContext
  ) throws -> [DeclSyntax] {
    return []
  }
}
