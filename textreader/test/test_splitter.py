import random
import string

from textreader.textsplitter import text_split, pivot_point, TextNode, TreeNode


def test_no_empties_or_too_long(ulysses):
    # GIVEN
    # WHEN
    result = text_split(ulysses, 280)

    # THEN
    assert '\ufeff' not in result[0]
    assert '' not in [x.strip() for x in result]
    assert max([len(x) for x in result]) < 280


def test_starts_with_heading(ulysses):
    # GIVEN
    # WHEN
    result = text_split(ulysses, 280)

    # THEN
    assert "ULYSSES" in result[0]
    assert "by James Joyce" in result[0]
    assert "-- I --" in result[0]


def test_last_is_paris(ulysses):
    # GIVEN
    # WHEN
    result = text_split(ulysses, 280)

    # THEN
    assert 'Trieste-Zurich-Paris 1914-1921' in result[-1]


def test_no_underscores(ulysses):
    # GIVEN
    # WHEN
    result = text_split(ulysses, 280)

    # THEN
    assert len([x for x in result if x.find("_") != -1]) == 0


def test_no_double_dash(ulysses):
    # GIVEN
    # WHEN
    result = text_split(ulysses, 280)

    # THEN
    assert len([x for x in result if x.find("--") != -1]) == 0


def test_double_dash_to_em_dash():
    # GIVEN
    # WHEN
    result = text_split("--", 280)

    # THEN
    assert "\u2014" in result


def test_last_sentence(ulysses):
    # GIVEN
    # WHEN
    result = text_split(ulysses, 280)

    # THEN
    assert "and first I put my arms around him yes and drew him down to me so he could feel my breasts all perfume yes and his heart was going like mad and yes I said yes I will Yes." in \
           result[-2]


def test_split_timo():
    # GIVEN
    # WHEN
    ti_mo = pivot_point("timo")

    # THEN
    assert ti_mo.total_length == 4
    assert ti_mo.split_at == 1
    assert ti_mo.left_part_length == ti_mo.right_part_length


def test_timo_node():
    # GIVEN
    ti_mo = TextNode(0, 3, pivot_point("timo"), 2, "timo")
    # WHEN
    tl, tr = TextNode.split(ti_mo)

    # THEN
    assert tl.start_index == 0
    assert tl.end_index == 1
    assert tr.start_index == 2
    assert tr.end_index == 3
    assert tl.full_text == tr.full_text
    assert tl.text + tr.text == tl.full_text


def test_timo_tree():
    # GIVEN
    ti_mo = TextNode(0, 3, pivot_point("timo"), 40, "timo")

    # WHEN
    timotree = TreeNode(ti_mo, None, None)

    # THEN
    assert timotree.ready
    assert ti_mo.full_text == "timo"


def test_split_node_tree():
    # GIVEN
    r = random.Random(1235)
    text = "".join([r.choice(string.ascii_letters) for x in range(128)])
    tn = TextNode.from_text(text, 32)

    # WHEN
    tree_node = TreeNode(tn, None, None)
    tree_node.handle()
    full_text = " ".join(tree_node.collect())

    # THEN
    assert full_text == tree_node.root_node.full_text


def test_split_ulysses_node_tree(ulysses):
    # GIVEN
    tn = TextNode.from_text(ulysses, 280)

    # WHEN
    tree_node = TreeNode(tn, None, None)
    tree_node.handle()
    collected = tree_node.collect()
    full_text = " ".join(collected)

    # THEN
    assert full_text == tree_node.root_node.full_text
    assert len(collected) == 123
