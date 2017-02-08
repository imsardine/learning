import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class App {

    private Greeting greeting;

    @Inject
    public App(Greeting greeting) {
        this.greeting = greeting;
    }

    public String helloWorld() {
        return greeting.greet("World");
    }

}

