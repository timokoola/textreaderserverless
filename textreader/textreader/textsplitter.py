import string
from typing import List, NamedTuple, Tuple

import math


def log_length_function(text, index):
    diff = (len(text) / 2 - 1) - index
    return math.log(abs(diff) + 1) + 1


def base_score(text: str, index: int) -> float:
    """Find a place to split string in two and in about two equal halves. Preference order:
    1. Newlines (score 16 / distance to the midpoint)
    2. "!.?" that is immediately followed by whitespace (score 16/ distance to the midpoint)
    3. Other punctuation immediately followed by whitespace (score 8/ distance to the midpoint)
    3. Other whitespace (score 2/ distance to the midpoint)
    4. Any other character (score 1/ distance to the midpoint)"""
    if 0 <= index < len(text):
        cur_char = text[index]
        prev_char = text[index - 1] if index - 1 > 0 else " "
        diff_to_center = log_length_function(text, index)
        if cur_char == "\n":
            return 16 / diff_to_center
        elif cur_char in string.whitespace and prev_char in "!?.":
            return 16 / diff_to_center
        elif cur_char in string.whitespace and prev_char in string.punctuation:
            return 8 / diff_to_center
        elif cur_char in string.whitespace:
            return 2 / diff_to_center
        else:
            return 1 / diff_to_center
    else:
        return -1


class PivotPoint(NamedTuple):
    """Represents a breaking point in a string"""
    split_at: int
    left_part_length: int
    right_part_length: int

    @property
    def total_length(self):
        return self.left_part_length + self.right_part_length


class TextNode(NamedTuple):
    # start index in the full text
    start_index: int
    # end index in the full text
    end_index: int
    split_point: PivotPoint
    max_length: int
    # always the full text
    full_text: str

    @classmethod
    def split(cls, node: 'TextNode') -> Tuple['TextNode', 'TextNode']:
        """Return left and right half of this tuple"""
        left_start = node.start_index
        left_end = left_start + node.split_point.split_at

        left = TextNode(left_start, left_end, pivot_point(node.full_text[left_start:left_end + 1]), node.max_length,
                        node.full_text)
        right = TextNode(left_end + 1, node.end_index, pivot_point(node.full_text[left_end + 1:node.end_index + 1]),
                         node.max_length, node.full_text)
        return left, right

    @property
    def text(self) -> str:
        return self.full_text[self.start_index:self.end_index + 1]

    @property
    def is_split_needed(self) -> bool:
        return (self.end_index + 1 - self.start_index) >= self.max_length

    @classmethod
    def from_text(cls, text, max_length) -> 'TextNode':
        return TextNode(0, len(text), pivot_point(text), max_length, text)


class TreeNode(NamedTuple):
    root_node: TextNode
    left_node: 'TreeNode'
    right_node: 'TreeNode'

    def collect(self) -> List['TextNode']:
        if not self.ready:
            self.handle()
        current = self
        result_stack = []  # type: List['TreeNode']
        leafs = []  # type: List['TreeNode']
        done = False
        while not done:
            if current is not None:
                result_stack.append(current)

                current = current.left_node
            else:
                if len(result_stack) > 0:
                    current = result_stack.pop()
                    leafs.append(current)
                    current = current.right_node
                else:
                    done = True
            print(len(result_stack), end=", ")
        return [x.root_node.text for x in leafs if x.is_leaf]

    @property
    def is_leaf(self) -> bool:
        return self.ready and self.left_node is None and self.right_node is None

    @property
    def ready(self) -> bool:
        left_ready = self.left_node is None or self.left_node.ready
        right_ready = self.right_node is None or self.right_node.ready

        return not self.root_node.is_split_needed or (left_ready and right_ready)

    def handle(self) -> None:
        if self.ready:
            pass
        else:
            left_text, right_text = TextNode.split(self.root_node)
            self.left_node = TreeNode(left_text, None, None)
            self.right_node = TreeNode(right_text, None, None)

            self.left_node.handle()
            self.right_node.handle()


def pivot_point(text: str) -> PivotPoint:
    """Find the breaking point for the string around the middle"""
    scores = [base_score(text, x[0]) for x in enumerate(text)]
    break_at = max([x for x in enumerate(scores)], key=lambda x: x[1])[0]
    return PivotPoint(break_at, len(text[:break_at + 1]), len(text[break_at + 1:]))


def text_split(text: str, max_length: int) -> List[str]:
    cleaned = clean_text(text)

    if len(cleaned) <= max_length:
        return [cleaned]

    if pivot_point(cleaned).total_length <= max_length:
        split_at = pivot_point(cleaned)
        return [cleaned[:split_at], cleaned[split_at:]]

    return [x for x in cleaned.split("\n") if len(x.strip()) > 0]


def clean_text(text: str) -> str:
    cleaned = text.replace("_", "")
    cleaned = cleaned.replace("--", "\u2014")
    cleaned = cleaned.replace("\s+", " ")
    cleaned = cleaned.replace("(\s\s+)", "\n")
    return cleaned
