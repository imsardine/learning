import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class GreetingImpl implements Greeting {

    @Inject
    public GreetingImpl() {
    }

    @Override
    public String greet(String who) {
        return "Hello, " + who + "!";
    }

}
