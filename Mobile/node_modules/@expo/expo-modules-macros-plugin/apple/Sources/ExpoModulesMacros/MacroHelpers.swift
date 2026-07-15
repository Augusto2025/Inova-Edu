import SwiftSyntax

/**
 Reads the first string-literal argument of an attribute, e.g. `@JS("doWork")` -> "doWork".
 Returns nil if the attribute has no arguments or the first argument is not a string literal.
 */
internal func jsNameArgument(of attribute: AttributeSyntax) -> String? {
  guard let args = attribute.arguments?.as(LabeledExprListSyntax.self),
    let first = args.first,
    let str = first.expression.as(StringLiteralExprSyntax.self),
    let segment = str.segments.first?.as(StringSegmentSyntax.self) else {
    return nil
  }
  return segment.content.text
}

/**
 Reads a labeled array-literal argument of an attribute, e.g. `@ExpoModule(classes: [Foo.self, Bar.self])`,
 and returns the type names referenced (e.g. `["Foo", "Bar"]`). Each element must be a
 `<TypeName>.self` member-access expression; non-conforming elements are skipped silently.
 */
internal func classListArgument(of attribute: AttributeSyntax, label: String) -> [String] {
  guard let args = attribute.arguments?.as(LabeledExprListSyntax.self) else {
    return []
  }
  for arg in args where arg.label?.text == label {
    guard let array = arg.expression.as(ArrayExprSyntax.self) else {
      return []
    }
    return array.elements.compactMap { element -> String? in
      guard let memberAccess = element.expression.as(MemberAccessExprSyntax.self),
        memberAccess.declName.baseName.text == "self",
        let base = memberAccess.base?.as(DeclReferenceExprSyntax.self) else {
        return nil
      }
      return base.baseName.text
    }
  }
  return []
}

extension AttributeListSyntax {
  internal func firstAttribute(named name: String) -> AttributeSyntax? {
    for element in self {
      if let attr = element.as(AttributeSyntax.self),
        attr.attributeName.trimmedDescription == name {
        return attr
      }
    }
    return nil
  }
}
