import org.junit.Test;
import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class DefaultAnswerTest {

    @Test
    public void returnsSelfForBuilders() {
        Config config = mock(Config.class, RETURNS_SELF);

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

