protocol Vehicle {
    var description: String { get }
    var numberOfWheels: Int { get }
    func accelerate()
}

extension Vehicle {

    // error: extensions may not contain stored properties
    // var somethingElse: String?

    var description: String {
        return "A vehicle with \(numberOfWheels) wheel(s)."
    }
}

class Bike: Vehicle {
    let numberOfWheels = 2

    func accelerate() {
    }
}

class Car: Vehicle {
    let numberOfWheels = 4

    func accelerate() {
    }
}

let bike = Bike(), car = Car()

print("Bike: \(bike.description)")
print("Car: \(car.description)")

