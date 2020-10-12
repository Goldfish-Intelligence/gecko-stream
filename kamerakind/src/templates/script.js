var calOptions = {
    defaultView: "week",
    taskView: false,
    template: {
        monthDayname: function (dayname) {
            return '<span class="calendar-week-dayname-name">' + dayname.label + '</span>';
        }
    },
    week: {
        startDayOfWeek: 1,
        daynames: ["sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"],
        hourStart: 10,
        hourEnd: 22,
        timezones: [{
            timezoneOffset: null,
            displayLabel: "Zeitzone Browser",
            isReadOnly: true,
            usageStatistics: false
        }]
    }
};
var calendar1 = new tui.Calendar('#calendar-1', calOptions);
var calendar2 = new tui.Calendar('#calendar-2', calOptions);
calendar2.setOptions({week: {workweek: true}});

calendar1.createSchedules([
    {% for event in events %}
    {
        id: "{{ event.id }}",
        calendarId: "1",

        category: "time",
        title: "{{ event.summary }}",
        start: "{{ event.start.dateTime }}",
        end: "{{ event.end.dateTime }}"
    },
    {% endfor %}
])

calendar2.createSchedules([
    {% for event in events %}
    {
        id: "{{ event.id }}",
        calendarId: "1",

        category: "time",
        title: "{{ event.summary }}",
        start: "{{ event.start.dateTime }}",
        end: "{{ event.end.dateTime }}"
    },
    {% endfor %}
])

calendar1.setDate("2020-10-19")
calendar2.setDate("2020-10-26")