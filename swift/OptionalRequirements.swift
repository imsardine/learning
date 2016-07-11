import Foundation

@objc protocol MyProtocol {
    func doSomething()
    optional func takeCustomAction(param: Int) -> String
    optional var customParam: Int { get }
}

class MyClass: NSObject, MyProtocol {

    let customParam = 3

    func doSomething() {
        print("Something finished!")
    }

}

let obj = MyClass()
obj.doSomething()

// obj.takeCustomAction?(3)
(obj as MyProtocol).takeCustomAction?(3)

