class MethodsWithSameNames {

    public static String hello(String who) {
        return "[Static] Hello, " + who;
    }

    // Uncomment the following (and comment the original method declaration),
    // you will see "method hello(java.lang.String) is already defined in class MethodsWithSameNames"
    //
    // public String hello(String who) {
    public String _hello(String who) {
        return "[Non-static] Hello, " + who;
    }

}
