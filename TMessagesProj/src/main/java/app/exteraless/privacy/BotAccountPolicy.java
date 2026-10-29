package app.exteraless.privacy;

/** Pure decision policy; a cached user or an empty dialog is not prior contact. */
public final class BotAccountPolicy {
    public static final int UNAVAILABLE = -1;
    public static final int AMBIGUOUS = -2;
    public static final int UNKNOWN = -3;

    private BotAccountPolicy() {}

    public static boolean isCurrent(long[] before, long[] now, long configuredBefore, long configuredNow,
                                    int activeBefore, int activeNow, boolean enabled) {
        return enabled && configuredBefore == configuredNow && activeBefore == activeNow && java.util.Arrays.equals(before, now);
    }

    public static int choose(boolean enabled, int requested, int configured, boolean explicit,
                             int[] established, boolean complete) {
        if (!enabled) return requested;
        if (explicit) {
            for (int account : established) {
                if (account == requested) return requested;
            }
        }
        if (!complete) return UNKNOWN;
        if (established.length == 1) return established[0];
        if (established.length > 1) return AMBIGUOUS;
        return configured < 0 ? UNAVAILABLE : configured;
    }
}
