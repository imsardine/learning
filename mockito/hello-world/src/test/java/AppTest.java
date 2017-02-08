import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class AppTest {

    @Test
    public void helloWorld() {
        Greeting greeting = mock(Greeting.class);
        when(greeting.greet("World")).thenReturn("Hello, World!");
        App app = new App(greeting);

        assertEquals("Hello, World!", app.helloWorld());
    }

}

