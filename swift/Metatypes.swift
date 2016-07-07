class SomeClass {
    func sayHello() -> String {
        // What's the difference between Metatypes.SomeClass and SomeClass
        return "Hello, I'm an instance of \(self) and/or \(self.dynamicType)."
    }
}

let someObject: AnyObject = SomeClass()
if someObject.dynamicType == SomeClass.self {
    print((someObject as! SomeClass).sayHello())
}

if let obj = someObject as? SomeClass {
    print(obj.sayHello())
}

