'''
    Views for calendar Widgets
'''

from PyQt5 import QtWidgets
from PyQt5 import QtGui


class EventInCalendar__View(QtWidgets.QLabel):
    '''
        Event description that appears in a calendar cell. It has the following format:
         ----------------------
        | HH:mm - HH:mm  Place |
         ----------------------
        That is: init time, end time and the place where the event will hold. Label
        color can be adjusted via a fulfillment criteria that ranges from 0 to 1,
        colors are:
        dark red:    [0.0 - 0.2)
        red:         [0.2 - 0.5)
        dark yellow: [0.5 - 0.7)
        yellow:      [0.7 - 1.0)
        green:       [1.0]
        The fulfillment criteria comes from the model function getFulFillmentStatus()
    '''

    def __init__(self, master, parent=None):
        QtWidgets.QLabel.__init__(self, parent=parent)

        self.master = master

        self.setMaximumHeight(50)

    def setText(self, richtext):
        '''
            Overrides super.setText. Here richtext is EventInCalendar__Model.Text class
            and has the parameters:
             * init_date: datetime.datetime()
             * end_date: datetime.datetime()
             * place: Event__Model.Place
            and has a __str__ method
        '''
        super(EventInCalendar__View, self).setText(str(richtext))

    def updateStatus(self):
        color = 'background-color: ' + self.master.getModel().getFulFillmentStatus()
        self.setStyleSheet(color)

    def updateFromModel(self):
        self.setText(self.master.getModel().__str__())
        self.updateStatus()


class Date__View(QtWidgets.QWidget):
    '''
        Date View of a date in the calendar, this element contains the EventInCalendar
        widgets and subclasses the QtWidgets.QWidget class
    '''

    def __init__(self, master, parent=None):
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setAutoFillBackground(True)

        # Date will organize events one on top of another vertically, so we will use
        # QVBoxLayout
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        # Instance master for later use
        self._master = master

        # Date number
        self._date = QtWidgets.QLabel()

        self.setMinimumHeight(200)
        self.update()

    def update(self):
        model = self._master.getModel()
        date = model.getDate().__str__()
        date = date.split('-')[0]

        # Remove leading zero
        if date and date[0] == '0':
            date = date[1:]

        # Update label
        self._date.setText(date)

        # Change background to reflect new datetype
        cdatetype = model.getDateType()

        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(*cdatetype))
        self.setPalette(p)

        # Remove all current EventsInDate from the view only
        events = model.getEvents()
        for event in events:
            try:
                self._layout(event.getView())
            except Exception:
                pass

        # Reorganize EventsInDate, sort by time, ascending
        events = model.getEvents()
        events.sort()

        # Add them back
        for event in events:
            self._layout.addWidget(event.getView())

    def updateFromModel(self):
        self.update()
