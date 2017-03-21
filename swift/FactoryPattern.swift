protocol Initable {
    init(name: String)
}

func createInstance<T: Initable>(type: T.Type, name: String) -> T {
    print("Type: \(type)")
    return type.init(name: name)
}

class A: Initable {

    var name: String

    required init(name: String) {
        self.name = name
    }

}

createInstance(A.self, name: "A")
createInstance(A.Type, name: "A.Type")

