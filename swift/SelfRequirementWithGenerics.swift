protocol Bootable<System> {
    func boot() -> System
}

extension Bootable<System> {
    func boot() -> System {
        print("Booting Unkown system ...")
        return self
    }
}

class SystemA: Bootable<SystemA> {
}

SystemA().boot()

