from pyglet.graphics import Batch, Group
from pyglet.text import Label

from .clickable_widget import Clickable
from .hoverable_widget import Hoverable
from shapes.rectangle import Rectangle


class Button(Label, Clickable, Hoverable):
    def __init__(self, text: str = '',
                 font_name: str = None, font_size: int = None, bold: bool = False, italic: bool = False,
                 color: tuple = (255, 255, 255, 255),
                 x: int = 0, y: int = 0, width: int = None, height: int = None,
                 anchor_x: str = 'left', anchor_y: str = 'baseline',
                 align: str = 'left',
                 multiline: bool = False, dpi: float = None, batch: Batch = None, group: Group = None,
                 padding: tuple = (0, 0, 0, 0)) -> None:
        """

        :param text:        The text to be displayed on the button
        :param font_name:   Name of the font to be used
        :param font_size:   Font size
        :param bold:        Sets the font style to bold if true
        :param italic:      Sets the font style to italic if true
        :param color:       Sets the color of the text
        :param x:           The x-coordinate with respect to the origin (0, 0
        :param y:
        :param width:
        :param height:
        :param anchor_x:
        :param anchor_y:
        :param align:
        :param multiline:
        :param dpi:
        :param batch:
        :param group:
        :param padding:
        """
        if len(padding) == 0:
            # No padding is supported, and nothing special will happen
            pass
        elif len(padding) == 1:
            # If only one padding value is supplied, it will be applied to all sides
            padding = (padding[0],) * 4
        elif len(padding) == 2:
            # If only two values (a, b) are supplied, a will be applied to top and bottom padding,
            # and b will be applied to left and right padding,
            # as  (a, b, a, b)
            padding = padding[0], padding[1], padding[0], padding[1]
        elif len(padding) == 4:
            pass
        else:
            # No other padding combination will work, so throw an error
            raise ValueError
        super().__init__(text,
                         font_name, font_size, bold, italic,
                         color,
                         x + padding[3], y + padding[2], width, height,
                         anchor_x, anchor_y,
                         align,
                         multiline, dpi, batch, group)  # Allow the Label superclass to __init__

        self.padding = padding

        # width of the label + padding on left and right
        self.width = self.content_width + self.padding[3] + self.padding[1]

        # height of the label + padding on the bottom and top
        self.height = self.padding[2] + self.content_height + self.padding[0]

        # The background color
        self.rectangle = Rectangle(
            x=x,
            y=y,
            width=self.width,
            height=self.height
        )

    def draw(self) -> None:
        # Draw the rectangle first so it's behind the label
        self.rectangle.draw()
        super().draw()
