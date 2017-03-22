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
    public void mockWrapperClass() {
        PowerMockito.mockStatic(Time.class);
        when(Time.now(any(String.class))).thenReturn(123L);

        assertEquals(123L, Time.now("mockWrapperClass"));

        PowerMockito.verifyStatic(); Time.now("mockWrapperClass");
    }

    @Test
    public void mockSystemClass() {
        PowerMockito.mockStatic(System.class);
        when(System.currentTimeMillis()).thenReturn(456L);

        assertEquals(456L, Time.now("mockSystemClass"));

        PowerMockito.verifyStatic(); System.currentTimeMillis();
    }

}

