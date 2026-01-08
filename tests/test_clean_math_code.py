import pytest

from scripts.clean_math_code import transform_text


def test_single_occurrence_on_line():
    text = "Before {{< math >}}$x+1${{< /math >}} after"
    new_text, count = transform_text(text)
    assert new_text == "Before $x+1$ after"
    assert count == 1


def test_multiple_occurrences_on_line():
    text = (
        "{{< math >}}$a${{< /math >}} and "
        "{{< math >}}$b + c${{< /math >}} end"
    )
    new_text, count = transform_text(text)
    assert new_text == "$a$ and $b + c$ end"
    assert count == 2


def test_multiline_shortcode_block_untouched():
    text = "{{< math >}}\n$x + y$\n{{< /math >}}"
    new_text, count = transform_text(text)
    assert new_text == text
    assert count == 0


def test_unrelated_math_shortcode_without_dollar_untouched():
    text = "Text with {{< math >}} placeholder {{< /math >}} but no inline math."
    new_text, count = transform_text(text)
    assert new_text == "Text with $ placeholder $ but no inline math."
    assert count == 1


def test_spacing_variations_in_shortcode_tags():
    text = "Start {{<  math   >}}   $x^2$   {{< / math >}} end"
    new_text, count = transform_text(text)
    assert new_text == "Start $x^2$ end"
    assert count == 1


def test_display_math_block_conversion():
    text = "\\[\nE = mc^2\n\\]\n"
    new_text, count = transform_text(text)
    expected = "{{< math >}}\n$\nE = mc^2\n$\n{{< /math >}}\n"
    assert new_text == expected
    assert count == 1


def test_inline_paren_math_conversion():
    text = "Energy \\(E = mc^2\\) is famous."
    new_text, count = transform_text(text)
    assert new_text == "Energy $E = mc^2$ is famous."
    assert count == 1


def test_multiline_dollar_block_conversion():
    text = "$$\nE = mc^2\n$$\n"
    new_text, count = transform_text(text)
    expected = "{{< math >}}\n$\nE = mc^2\n$\n{{< /math >}}\n"
    assert new_text == expected
    assert count == 1


def test_shortcode_block_without_dollars_adds_dollar_lines():
    text = "{{< math >}}\nE = mc^2\n{{< /math >}}\n"
    new_text, count = transform_text(text)
    expected = "{{< math >}}\n$\nE = mc^2\n$\n{{< /math >}}\n"
    assert new_text == expected
    assert count == 1


def test_inline_shortcode_without_dollars_adds_inline_dollars():
    text = "Inline {{< math >}}x_t{{< /math >}} here."
    new_text, count = transform_text(text)
    assert new_text == "Inline $ x_t $ here."
    assert count == 1
