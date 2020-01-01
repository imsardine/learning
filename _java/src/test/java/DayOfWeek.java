public enum DayOfWeek {
    MONDAY    (false),
    TUESDAY   (false),
    WEDNESDAY (false),
    THURSDAY  (false),
    FRIDAY    (false),
    SATURDAY  (true),
    SUNDAY    (true);

    private boolean weekend;

    private DayOfWeek(boolean weekend) {
        this.weekend = weekend;
    }

    public boolean weekend() {
        return weekend;
    }

}

