import org.junit.Test;
import static org.junit.Assert.*;

public class GreetingImplTest {

    @Test
    public void greet() {
        Greeting greeting = new GreetingImpl();
        assertEquals("Hello, World!", greeting.greet("World"));
    }

}

