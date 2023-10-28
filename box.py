from enum import Enum
import pygame
from uiClass import UiElement, UiElementGroup, Color, Direction
from typing import Callable


X = 0
Y = 1


class OverflowingOptions(Enum):
    resize_text = 0
    resize_box_down = 1
    resize_box_right = 2
    allow_overflow = 3


class Box(UiElement):
    """Box with background and boarder colors."""
    def __init__(
            self,
            display_surface: pygame.surface.Surface,
            position_function: Callable[[int, int], tuple[int, int]],
            size_function: Callable[[int, int], tuple[int, int]],
            background_color: Color,

            focused_color: str,

            corner_rounding_amount: int,

            border_color: str,
            border_size: int,

            draw_from: 'Direction',

            fill_in_border: bool,
    ) -> None:
        super().__init__(display_surface, position_function, size_function)
        self.background_color = background_color
        self.focused_color = focused_color
        self.corner_rounding_amount = corner_rounding_amount
        self.border_color = border_color
        self.border_size = border_size
        self.draw_from = draw_from
        self.fill_in_border = fill_in_border

    def draw(self):
        if self.draw_from == Direction.center:
            self.set_position((self.position[X] - self.size[X], self.position[Y] - self.size[Y]))

        if (self.fill_in_border and self.border_size) or not self.border_size:
            color = self.focused_color if self.is_hovered_over or self.is_selected else self.background_color
            pygame.draw.rect(self.display_surface, color, self.rect, 0, self.corner_rounding_amount)

        if self.border_size:
            pygame.draw.rect(
                self.display_surface, self.border_color, self.rect, self.border_size, self.corner_rounding_amount
            )

    def set_position(self, position: tuple[int, int]):
        self.position = position

    def move(self, displacement: tuple[int, int]):
        self.position = self.position[X] + displacement[X], self.position[Y] + displacement[Y]

    def set_background_color(self, color):
        self.background_color = color


class Image(UiElement):
    """An image drawn on top of a box."""
    def __init__(
            self,
            image_path: str,
            blending_type: int,
            margin: int,
            box: 'Box',

            resize_image_to_box: bool = True,
            center_image_in_box: bool = True,
            keep_image_proportion: bool = True,
    ) -> None:
        super().__init__(box.display_surface, box.position_function, box.size_function)
        self.image_path = image_path
        self.blending_type = blending_type
        self.box = box
        self.margin = margin

        self.resize_image_to_box = resize_image_to_box
        self.center_image_in_box = center_image_in_box
        self.keep_image_proportion = keep_image_proportion

    def draw(self):
        self.box.draw()
        
        image = pygame.image.load(self.image_path)  # retrieving image
        if self.keep_image_proportion and self.resize_image_to_box:
            scale_up = min(
                (self.rect.width - self.margin) / image.get_width(),
                (self.rect.height - self.margin) / image.get_height()
            )
            image = pygame.transform.scale(image, image.get_rect().scale_by(scale_up, scale_up).size)
        elif self.resize_image_to_box:
            display_area = self.box.rect.width - self.margin, self.box.rect.height - self.margin
            image = pygame.transform.scale(image, display_area)  # scaling image
        image_size = image.get_size()  # getting size
        image = image.convert_alpha()  # removing transparent parts of image

        if self.center_image_in_box:  # centering the image
            pos = (self.rect.center[0] - image_size[0] / 2 + 1, self.rect.center[1] - image_size[1] / 2 + 1)
        else:  # putting the image on the top left
            pos = self.rect.topleft

        # rounding the corners of the image if it is resized
        flag = self.blending_type if self.resize_image_to_box else 0
        self.display_surface.blit(image, pos, None, flag)
        

    def update(self, event):
        self.box.update(event)
        super().update(event)

    def set_position(self, position: tuple[int, int]):
        self.box.set_position(position)

    def move(self, displacement: tuple[int, int]):
        self.box.move(displacement)


class TextBox(UiElement):
    # the text after it has been interpreted
    __text_by_line = None

    # the images of the text after it has been rendered
    __images_by_line = None

    def __init__(
            self,
            text: str,
            text_color: 'Color',
            text_size: int,
            text_font: str,
            text_wrap: bool,
            text_justification: 'Direction',
            if_overflowing_text: 'OverflowingOptions',
            resize_box_to_text: bool,
            margin: int,

            box: 'Box'
    ) -> None:
        super().__init__(box.display_surface, box.position_function, box.size_function)
        self.text = text
        self.text_color = text_color
        self.text_size = text_size
        self.text_font = text_font
        self.text_wrap = text_wrap
        self.text_justification = text_justification
        self.if_overflowing_text = if_overflowing_text
        self.resize_box_to_text = resize_box_to_text

        self.margin = margin

        self.box = box

    def draw(self):
        if self.__text_by_line is None:
            self.__text_by_line = self.interpret_text()
        if self.__images_by_line is None:
            self.__images_by_line = self.convert_text_to_images()
            self.overflow()

        self.box.draw()
        
        top_justification = [Direction.topleft, Direction.midtop, Direction.topright]
        mid_ver_justification = [Direction.midleft, Direction.midright, Direction.center]

        left_justification = [Direction.topleft, Direction.midleft, Direction.bottomleft]
        mid_hor_justification = [Direction.midtop, Direction.center, Direction.midbottom]

        # total height of the text
        total_image_height = sum(max(image.get_height() for image in line) for line in self.__images_by_line)

        # handling the height offset between the lines:
        if self.text_justification in top_justification:
            vertical_offset = 0
        elif self.text_justification in mid_ver_justification:
            vertical_offset = (total_image_height * (1 / len(self.__images_by_line) - 1)) / 2
        else:  # justification is bottom left, right, or middle
            vertical_offset = -total_image_height + max(image.get_height() for image in self.__images_by_line[-1])

        for i, line in enumerate(self.__images_by_line):
            total_image_width = sum(image.get_width() for image in line)
            if self.text_justification in left_justification:
                horizontal_offset = 0
            elif self.text_justification in mid_hor_justification:
                horizontal_offset = (-total_image_width + line[0].get_width()) / 2
            else:  # justification is top right, middle right, bottom right
                horizontal_offset = -total_image_width + line[0].get_width()

            for j, image in enumerate(line):
                # used to center the text within its line
                if self.text_justification in top_justification:
                    addition = (max(img.get_height() for img in line) - image.get_height()) / 2
                elif self.text_justification in mid_ver_justification:
                    addition = 0
                else:
                    addition = -(max(img.get_height() for img in line) - image.get_height()) / 2
                blit_pos = self.justify_text(image, vertical_offset + addition, horizontal_offset)

                # handling width
                if j < len(line) - 1:
                    if self.text_justification in left_justification:
                        horizontal_offset += image.get_width()
                    elif self.text_justification in mid_hor_justification:
                        horizontal_offset += (image.get_width() + line[j + 1].get_width()) / 2
                    else:  # justification is top right, middle right, bottom right
                        horizontal_offset += line[j + 1].get_width()

                # drawing the text
                self.display_surface.blit(image, blit_pos)

            # handling height
            if i < len(self.__images_by_line) - 1:
                if self.text_justification in top_justification:
                    vertical_offset += max(image.get_height() for image in line)
                elif self.text_justification in mid_ver_justification:
                    vertical_offset += (max(image.get_height() for image in line) +
                                        max(image.get_height() for image in self.__images_by_line[i + 1])) / 2
                else:
                    vertical_offset += max(image.get_height() for image in self.__images_by_line[i + 1])

    def convert_text_to_images(self) -> list[list[pygame.surface.Surface]]:
        """
        Converts text with its properties into images of the text.

        :returns: A list of lines which have images of the text
        """

        lines: list[list[pygame.surface.Surface]] = []
        for line in self.__text_by_line:
            used_space = 0  # space already taken up in each line (0 for a new line, >0 for a continuation)

            if not self.text_wrap:
                lines.append([self.render_text(*text_and_properties) for text_and_properties in line])
                continue

            for text_and_properties in line:
                # looping while there is leftover on each line after wrapping
                # if there is a continuation, only allow wrapping by word                    ˅˅˅˅˅˅˅˅˅˅˅˅˅˅
                while (image_and_leftover := self.wrap_text(text_and_properties, used_space, not used_space))[1]:
                    # in the loop, is the image of the rendered text which can fit in the text box
                    # and the text that was left over and needs to be placed in another line

                    image, leftover = image_and_leftover  # image and leftover text

                    if image is None:  # go to the next line, the text cannot be wrapped by word
                        if not used_space:
                            return [
                                [self.render_text('Sorry,', self.default_properties)],
                                [self.render_text('window', self.default_properties)],
                                [self.render_text('is too', self.default_properties)],
                                [self.render_text('small', self.default_properties)]
                            ]
                        used_space = 0
                        continue

                    text_and_properties = (leftover.strip(' '), text_and_properties[1])

                    if used_space == 0:  # if this is on a new line, display the image in the next line
                        lines.append([image])
                    else:  # if this is a continuation of the previous line, display the image on the previous line
                        lines[-1].append(image)
                        used_space = 0  # the program moves to a new line

                if image_and_leftover[0].get_width() == 0:  # image is of ' ', skip it
                    continue

                # if this was a continuation of the previous line, add the image to the previous line
                if used_space:
                    lines[-1].append(image_and_leftover[0])

                # this was not a continuation of the previous line, add the image to a new line
                else:
                    lines.append([image_and_leftover[0]])
                used_space += image_and_leftover[0].get_width()  # the program continues from this line

        return lines

    def overflow(self) -> None:
        text_and_properties: list[dict]
        # checking if text does not overflow:
        if self.if_overflowing_text is OverflowingOptions.allow_overflow:
            return
        height_of_lines = sum(max(image.get_height() for image in line) for line in self.__images_by_line)
        if not self.resize_box_to_text and height_of_lines <= self.rect.height - 2 * self.margin:
            return

        # handling overflow:
        # TODO: resize_text needs to be further tested and have it's speed improved
        if self.if_overflowing_text == OverflowingOptions.resize_text:
            # need to increment/decrement the sizes of text so that it fits in the box
            # if the size of the text is 1, then end the decrementing and state that the text cannot be displayed
            print(self.__text_by_line)

            target = self.rect.height - 2 * self.margin

            if height_of_lines == target:  # nothing needs to be resized
                return
            while height_of_lines < target:  # text needs to be resized up
                for line in self.__text_by_line:
                    for text_and_properties in line:
                        text_and_properties[1]['s'] += 1
                lines = self.convert_text_to_images()
                self.__images_by_line = lines
                height_of_lines = sum(max(image.get_height() for image in line) for line in lines)
            while height_of_lines > target:  # text needs to be resized down
                for line in self.__text_by_line:
                    for text_and_properties in line:
                        if text_and_properties[1]['s'] <= 1:
                            self.__images_by_line = self.error_message
                            return
                        text_and_properties[1]['s'] -= 1
                lines = self.convert_text_to_images()
                self.__images_by_line = lines
                height_of_lines = sum(max(image.get_height() for image in line) for line in lines)
        elif self.if_overflowing_text == OverflowingOptions.resize_box_down:
            self.rect.height = height_of_lines + 2 * self.margin
        else:  # resize box to the right
            # TODO: change the width of the box according to the text
            self.rect.width *= height_of_lines / (self.rect.height - 2 * self.margin)
            self.convert_text_to_images()

    def justify_text(
            self,
            image: pygame.surface.Surface,
            vertical_offset: int,
            horizontal_offset: int
    ) -> pygame.rect.Rect:
        """Returns the position to display the text."""
        left = self.rect.left + self.margin + horizontal_offset
        mid_horizontal = self.rect.centerx + horizontal_offset
        right = self.rect.right - self.margin + horizontal_offset

        top = self.rect.top + self.margin + vertical_offset
        mid_vertical = self.rect.centery + vertical_offset
        bottom = self.rect.bottom - self.margin + vertical_offset

        justification_to_position = {
            Direction.topleft: image.get_rect(topleft=(left, top)),
            Direction.midtop: image.get_rect(midtop=(mid_horizontal, top)),
            Direction.topright: image.get_rect(topright=(right, top)),

            Direction.midleft: image.get_rect(midleft=(left, mid_vertical)),
            Direction.center: image.get_rect(center=(mid_horizontal, mid_vertical)),
            Direction.midright: image.get_rect(midright=(right, mid_vertical)),

            Direction.bottomleft: image.get_rect(bottomleft=(left, bottom)),
            Direction.midbottom: image.get_rect(midbottom=(mid_horizontal, bottom)),
            Direction.bottomright: image.get_rect(bottomright=(right, bottom)),
        }
        return justification_to_position[self.text_justification]

    def wrap_text(self, text_and_properties: list[str, dict], used_space, char_wrap: bool = True) \
            -> tuple:

        text, properties = text_and_properties
        leftover = ''

        while (image := self.render_text(text, properties)).get_width() > self.line_length() - used_space:
            if len(text) == 1:
                return None, text
            i = text.rfind(' ')
            if i == -1 or i == 0:
                if not char_wrap:
                    return None, text
                i = len(text) - 1
            leftover = text[i:] + leftover
            text = text[:i]

        return image, leftover

    def line_length(self, position: None = None, width = None):
        # TODO: additional logic is needed to calculate the length of a line on a curved box
        return self.rect.width - 2 * self.margin

    @staticmethod
    def render_text(text: str, properties: dict[str, ]) -> pygame.surface.Surface:
        """Renders text."""
        font = pygame.font.SysFont(properties['f'], properties['s'], bold=properties['b'], italic=properties['i'])
        return font.render(text, True, properties['c'])

    def interpret_text(self) -> list[list[list[str, dict], ], ] :
        # noinspection GrazieInspection
        """
        Interprets `self.text`, changing properties of text between tags and separating `self.text` into different
        lines. Tags are denoted with angle brackets "<>" with the properties being denoted using the below format:
            PROPERTY:VALUE (special cases are with the properties bold and italic)
        ex.
        - "<c: green, s: 20, f: arial, b>Yes</>\n<S:20,f: arial, I>This means you agree</>"

          (Yes; color is green, size is 20, font is arial, bolded)
          (This means you agree; size is 20, font is arial, italic)

        - '''UC<     c      : green,        s: 20, f: arial, b>Yes</>UC<c:blue>BLUE</>UC
<            >UC<c:blue>BLUE</>UC<S:20,f:      ARIAL, I>This means <
             >you agree</>UC<c:blue>BLUE</>UC
<            >UC<c:blue>BLUE</>UC<i>ITALIC</>UC'''

          UC(Yes; color is green, size is 20, font is arial, bolded)UC(BLUE; color is blue)UC
          UC(BLUE; color is BLUE)UC(This means you agree; size is 20, font is arial, italic)UC(BLUE; color is blue)UC
          UC(BLUE; color is blue)UC(ITALIC; italic)UC
          """
        default_properties = self.default_properties

        # removing unwanted whitespaces:
        i = 0
        processed_text = ''
        while i < len(self.text):
            if self.text[i] == '<':
                starting_i = i
                i += 1
                while self.text[i] in ' \n':
                    i += 1
                if self.text[i] != '>':
                    processed_text += self.text[starting_i: i + 1]
                i += 1
                continue
            processed_text += self.text[i]
            i += 1
        self.text = processed_text

        text_segments: list[list[str, dict], ] = [  # splitting the text up and adding default properties to them
            [text_segment, default_properties.copy()] for text_segment in self.text.split('\n')
        ]
        # list of lines containing text segments and properties
        text_by_line: list[list[list[str, dict], ], ] = []
        # for tags that cover multiple lines, properties are "continued"
        continued_properties = default_properties.copy()

        # each loop processes a line
        for text_segment, segment_properties in text_segments:  # `text_segment`: str, `segment_properties`: dict
            text_by_line.append([])  # adding a new line
            add_processed_text = lambda __processed_text: text_by_line[-1].append(__processed_text)  # helper function

            # each loop processes a tag
            while text_segment.count('<') > 0 and text_segment.count('>') > 0:

                tag_start = text_segment.find('<')
                tag_end = text_segment.find('>')
                tag_contents = text_segment[tag_start + 1:tag_end].lower().replace(' ', '')

                # adding the text before tags to `interpreted_text` and removing processed segments of it:
                # the text before an ending tag has its properties continued
                # the text before a starting tag has default properties
                text_before_properties = continued_properties if tag_contents == '/' else default_properties
                if tag_start != 0:  # has text before the tag
                    add_processed_text([text_segment[:tag_start], text_before_properties])
                text_segment = text_segment[tag_end + 1:]  # remove the tag and anything before it (it was processed)
                if tag_contents == '/':
                    continue  # end tags have no properties to process, so continue

                # setting segment properties to the correct values:
                for key_value_pair in tag_contents.split(','):  # `key_value_pair` is a string like this: 's:20'
                    key, _, value = key_value_pair.partition(':')  # `key` = 's', `value` = '20'
                    key = key[0]
                    if key == 'b' or key == 'i':
                        value = True  # bold or italic
                    elif key == 's':
                        value = int(value)  # size
                    else:
                        value = value.replace('-', ' ')  # color or font
                    segment_properties[key] = value

                # adding the text inside the tags to `interpreted_text`:
                text = text_segment[:text_segment.find('</>')] if '</>' in text_segment else text_segment  # text to add
                add_processed_text([text, segment_properties])
                if '</>' in text_segment:  # there is an end tag
                    text_segment = text_segment[text_segment.find('</>') + 3:]  # removing processed values
                    segment_properties = default_properties.copy()  # resetting `segment_properties`
                    continue

                # there is not an end tag
                continued_properties = segment_properties.copy()  # continuing `segment_properties`
                text_segment = ''  # all values processed, reset `text_segment`

            if text_segment:  # adding all unprocessed values
                if continued_properties != default_properties:
                    add_processed_text([text_segment, continued_properties])
                else:
                    add_processed_text([text_segment, default_properties])
        return text_by_line

    @property
    def error_message(self) -> list[list[pygame.surface.Surface, ], ]:
        return [
            [self.render_text('Sorry,', self.default_properties)],
            [self.render_text('window', self.default_properties)],
            [self.render_text('is too', self.default_properties)],
            [self.render_text('small', self.default_properties)]
        ]

    @property
    def default_properties(self) -> dict[str, bool ]:
        return {  # the default properties of text
            'b': False,  # bold  bool
            'i': False,  # italic  bool
            'c': self.text_color,  # color  str
            'f': self.text_font,  # font  str
            's': self.text_size  # size  int
        }

    def set_position(self, position: tuple[int, int]):
        self.box.set_position(position)

    def move(self, displacement: tuple[int, int]):
        self.box.move(displacement)

    def set_text(self, text: str) -> 'TextBox':
        self.__text_by_line = None
        self.__images_by_line = None
        self.text = text

        return self


class ChooseOneGroup(UiElementGroup):
    def __init__(self, *args: UiElement):
        super().__init__(*args)

    def update(self, event: pygame.event.Event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            super().update(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            selected_element = None

            for element in self.elements:
                if element.is_hovered_over:
                    self.select_element(element)
                    selected_element = element
                    break
            return None if selected_element is None else selected_element.stored_value

    def select_element(self, element_to_select):
        for element in self.elements:
            if element is element_to_select:
                element.is_selected = True
            else:
                element.is_selected = False
