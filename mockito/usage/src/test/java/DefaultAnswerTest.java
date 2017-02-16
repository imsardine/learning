import org.junit.Test;
import org.junit.Rule;
import org.mockito.Mock;
import org.mockito.Answers;
import org.mockito.junit.MockitoJUnit;
import org.mockito.junit.MockitoRule;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class DefaultAnswerTest {

    @Rule
    public MockitoRule mockito = MockitoJUnit.rule();

    @Mock(answer = Answers.RETURNS_SELF)
    private Config config;

    @Test
    public void returnsSelfForBuilders_InlineMock() {
        Config config = mock(Config.class, RETURNS_SELF);

        Config configReturned = config.arg1("arg1").arg2("arg2");

        assertSame(configReturned, config);
        assertNull(config.toString());
    }

    @Test
    public void returnsSelfForBuilders_AnnotationMock() {
        Config configReturned = config.arg1("arg1").arg2("arg2");

        assertSame(configReturned, config);
        assertNull(config.toString());
    }

    private class Config { // Builder

        private String arg1;

        private String arg2;

        public Config arg1(String arg1) {
            this.arg1 = arg1;
            return this;
        }

        public Config arg2(String arg2) {
            this.arg2 = arg2;
            return this;
        }

    }

}

