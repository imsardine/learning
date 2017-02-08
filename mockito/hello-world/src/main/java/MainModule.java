import dagger.Module;
import dagger.Provides;

@Module
public class MainModule {

    @Provides
    public Greeting provideGreeting(GreetingImpl impl) {
        return impl;
    }

}
