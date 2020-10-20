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
    },
    useDetailPopup: true,
    theme: {
        'common.backgroundColor': 'rgba(0,0,0,0.25)'
        /*
        'common.border': '1px solid #2a3137',
        'common.backgroundColor': 'rgba(0,0,0,0.25)',
        'week.timegridLeft.backgroundColor': 'rgba(255,255,225,0.25)',
        'week.dayname.borderTop': 'inherit',
        'week.dayname.borderBottom': 'inherit',
        'week.dayname.borderLeft': 'inherit',
        'week.vpanelSplitter.border': 'inherit',
        'week.daygrid.borderRight': 'inherit',
        'week.daygridLeft.borderRight': 'inherit',
        'week.timegridLeft.borderRight': 'inherit',
        'week.timegridHalfHour.borderBottom': 'inherit',
        'week.timegridHorizontalLine.borderBottom': 'inherit',*/
    },
    template: {
        popupDetailBody: function(schedule) {
            htmlResult = "";
            if (schedule.raw.ignore) {
                htmlResult += "<p class='event-ignore'>Kein YouTube Stream</p>"
            }
            if (schedule.raw.location) {
                htmlResult += "<a href='" + schedule.raw.location + "'>Aufzeichnung</a><br>"
            }
            htmlResult += schedule.body;

            return htmlResult;
        }
    }
};
var calendar1 = new tui.Calendar('#calendar-1', calOptions);
var calendar2 = new tui.Calendar('#calendar-2', calOptions);
calendar2.setOptions({ week: { workweek: true } });

calendar1.createSchedules([
    {% for event in events %}
        {
            id: "{{ event.id }}",
            calendarId: "1",
            bgColor: "{{ event.calendarBgColor }}",

            category: "time",
            title: "{{ event.summary }}",
            body: `{{ event.description | safe }}`,
            raw: {
                ignore: {{ event.ignore | tojson }},
                {% if event.location %}
                    location: "{{ event.location }}"
                {% endif %}
            },
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
            bgColor: "{{ event.calendarBgColor }}",

            category: "time",
            title: "{{ event.summary }}",
            body: `{{ event.description | safe }}`,
            raw: {
                ignore: {{ event.ignore | tojson }}
            },
            start: "{{ event.start.dateTime }}",
            end: "{{ event.end.dateTime }}"
        },
    {% endfor %}
])

calendar1.setDate("2020-10-19")
calendar2.setDate("2020-10-26")