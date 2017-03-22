import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.powermock.api.mockito.PowerMockito;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;
import org.powermock.modules.junit4.rule.PowerMockRule;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;
import static org.powermock.api.mockito.PowerMockito.mockStatic;
import static org.powermock.api.mockito.PowerMockito.verifyStatic;

@PrepareForTest(Time.class)
public class StaticMethodRuleTest {

    @Rule
    public PowerMockRule powerMockRule = new PowerMockRule();

    @Test
    public void mockStaticMethods() {
        PowerMockito.mockStatic(Time.class);
        when(Time.now()).thenReturn(456L);

        assertEquals(456L, Time.now());

        PowerMockito.verifyStatic(); Time.now();
    }

}

