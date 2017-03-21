protocol Bootable {
    func boot() -> Self
}

extension Bootable {

    func boot() -> Self {
        print("Booting System? ...")
        return self
    }

}

final class SystemA: Bootable {

    let propertySpecificToA = "Blah blah ... A"

    func boot() -> SystemA {
        print("Booting SystemA ...")
        return self
    }
  
}

final class SystemB: Bootable {

    let propertySpecificToB = "Blha blah ... B"

    func boot() -> SystemB {
        print("Booting SystemB ...")
        return self
    }
  
}

final class SystemC: Bootable {

    let propertySpecificToC = "Blha blah ... C"
  
}

let a = SystemA()
let b = SystemB()
let c = SystemC()

print(a.boot().propertySpecificToA)
print(b.boot().propertySpecificToB)
print(c.boot().propertySpecificToC)

