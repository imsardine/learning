import org.junit.Test;
import org.junit.Before;
import static org.junit.Assert.*;

public class MainTest {

    private App app;

    @Before
    public void setUp() {
        MainComponent component = DaggerMainComponent.create();
        app = component.app();
    }

    @Test
    public void helloWorld() {
        assertEquals("Hello, World!", app.helloWorld());
    }

}

