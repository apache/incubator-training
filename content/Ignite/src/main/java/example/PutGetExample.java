package example;

import org.apache.ignite.Ignite;
import org.apache.ignite.IgniteCache;
import org.apache.ignite.Ignition;
import org.apache.ignite.configuration.IgniteConfiguration;

public class PutGetExample {
    public static void main(String[] args) {

        IgniteConfiguration cfg = new IgniteConfiguration();
        cfg.setClientMode(true);

        try (Ignite ignite = Ignition.start(cfg)) {
            // tag::contains[]
            IgniteCache<Integer, String> cache = ignite.getOrCreateCache("myCacheName");

            // Store keys in cache (values will end up on different cache nodes).
            for (int i = 0; i < 10; i++)
                cache.put(i, Integer.toString(i));

            for (int i = 0; i < 10; i++)
                System.out.println("Got [key=" + i + ", val=" + cache.get(i) + ']');
            // end::contains[]
        }
    }
}
