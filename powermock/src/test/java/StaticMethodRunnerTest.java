import org.junit.Test;
import org.junit.runner.RunWith;
import org.powermock.api.mockito.PowerMockito;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import static org.powermock.api.mockito.PowerMockito.mockStatic;
import static org.powermock.api.mockito.PowerMockito.verifyStatic;

@RunWith(PowerMockRunner.class)
@PrepareForTest(Time.class)
public class StaticMethodRunnerTest {

    @Test
    public void mockStaticMethods() {
        PowerMockito.mockStatic(Time.class);
        when(Time.now()).thenReturn(123L);

        assertEquals(123L, Time.now());

        PowerMockito.verifyStatic(); Time.now();
    }

}

