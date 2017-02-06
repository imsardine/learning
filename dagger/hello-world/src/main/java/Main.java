public class Main {

    public static void main(String[] args) {
        MainComponent component = DaggerMainComponent.create();
        System.out.println(component.app().helloWorld());
    }

}
