from api.main import SectionResult, build_rag_prompt


def test_prompt_includes_question():
    sections = [
        SectionResult(
            section_num="1946",
            citation_url="https://example.com",
            raw_text="Landlords must give notice.",
            summary="Notice rule",
            score=0.9,
        )
    ]
    prompt = build_rag_prompt("Can my landlord evict me without notice?", sections)

    assert "Can my landlord evict me without notice?" in prompt
    assert "1946" in prompt
    assert "Landlords must give notice." in prompt


def test_prompt_formats_multiple_sections():
    sections = [
        SectionResult(
            section_num="1946",
            citation_url="x",
            raw_text="Text A",
            summary="s",
            score=0.9,
        ),
        SectionResult(
            section_num="1950",
            citation_url="x",
            raw_text="Text B",
            summary="s",
            score=0.8,
        ),
    ]
    prompt = build_rag_prompt("question", sections)

    assert "§ 1946" in prompt
    assert "§ 1950" in prompt
    assert "Text A" in prompt
    assert "Text B" in prompt


def test_prompt_instructs_model_not_to_give_legal_advice():
    sections = [
        SectionResult(
            section_num="1946",
            citation_url="x",
            raw_text="Text",
            summary="s",
            score=0.9,
        ),
    ]
    prompt = build_rag_prompt("question", sections)

    assert "NOT a lawyer" in prompt
    assert "legal advice" in prompt


def test_prompt_specifies_json_output_format():
    sections = [
        SectionResult(
            section_num="1946",
            citation_url="x",
            raw_text="Text",
            summary="s",
            score=0.9,
        ),
    ]
    prompt = build_rag_prompt("question", sections)

    assert '"answer"' in prompt
    assert '"cited_sections"' in prompt
