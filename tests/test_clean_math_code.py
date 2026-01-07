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
    assert new_text == text
    assert count == 0


def test_spacing_variations_in_shortcode_tags():
    text = "Start {{<  math   >}}   $x^2$   {{< / math >}} end"
    new_text, count = transform_text(text)
    assert new_text == "Start $x^2$ end"
    assert count == 1
