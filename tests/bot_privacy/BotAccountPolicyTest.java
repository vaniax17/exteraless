package app.exteraless.privacy;

public class BotAccountPolicyTest {
    public static void main(String[] args) {
        check(0, BotAccountPolicy.choose(false, 0, -1, false, new int[]{}, true));
        check(1, BotAccountPolicy.choose(true, 0, 1, false, new int[]{}, true));
        check(0, BotAccountPolicy.choose(true, 0, 1, false, new int[]{0}, true));
        check(0, BotAccountPolicy.choose(true, 0, 2, true, new int[]{0, 1}, true));
        check(BotAccountPolicy.AMBIGUOUS, BotAccountPolicy.choose(true, 0, 2, false, new int[]{0, 1}, true));
        check(1, BotAccountPolicy.choose(true, 0, 2, true, new int[]{1}, true));
        check(BotAccountPolicy.UNAVAILABLE, BotAccountPolicy.choose(true, 0, -1, false, new int[]{}, true));
        check(BotAccountPolicy.UNKNOWN, BotAccountPolicy.choose(true, 0, 1, false, new int[]{}, false));
        check(0, BotAccountPolicy.choose(true, 0, -1, true, new int[]{0}, true));
        check(0, BotAccountPolicy.choose(true, 0, 1, true, new int[]{0}, false));
        check(BotAccountPolicy.UNKNOWN, BotAccountPolicy.choose(true, 0, 1, false, new int[]{0}, false));
        // Changing the configured or active account cannot migrate established dialogs.
        for (int active = 0; active < 3; active++) {
            for (int configured = 0; configured < 3; configured++) {
                check(0, BotAccountPolicy.choose(true, active, configured, false, new int[]{0}, true));
                check(configured, BotAccountPolicy.choose(true, active, configured, false, new int[]{}, true));
            }
        }
        long[] ids = {111L, 222L, 0L};
        if (!BotAccountPolicy.isCurrent(ids, ids.clone(), 222L, 222L, 0, 0, true)) throw new AssertionError();
        if (BotAccountPolicy.isCurrent(ids, new long[]{111L, 333L, 0L}, 222L, 222L, 0, 0, true)) throw new AssertionError("slot reused after logout");
        if (BotAccountPolicy.isCurrent(ids, ids, 222L, 111L, 0, 0, true)) throw new AssertionError("setting changed");
        if (BotAccountPolicy.isCurrent(ids, ids, 222L, 222L, 0, 1, true)) throw new AssertionError("active account changed");
        if (BotAccountPolicy.isCurrent(ids, ids, 222L, 222L, 0, 0, false)) throw new AssertionError("feature disabled");
        System.out.println("BotAccountPolicy: all cases passed");
    }
    private static void check(int expected, int actual) {
        if (expected != actual) throw new AssertionError(expected + " != " + actual);
    }
}
