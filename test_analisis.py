from analisis import menciona


def test_encuentra_la_palabra_sola():
    assert menciona("We use AI every day", "AI")


def test_la_encuentra_aunque_tenga_una_coma_al_lado():
    assert menciona("Experience with AI, SQL and Python", "AI")


def test_la_encuentra_al_empezar_la_oracion():
    assert menciona("AI tools are a plus", "AI")


def test_no_cuenta_maintain_como_AI():
    assert not menciona("You will maintain the system", "AI")


def test_no_cuenta_email_ni_detail_como_AI():
    assert not menciona("Send an email with the details", "AI")


def test_no_cuenta_excellent_como_Excel():
    assert not menciona("Excellent communication skills", "Excel")


def test_no_cuenta_digital_como_Git():
    assert not menciona("Digital marketing experience", "Git")


def test_aguanta_una_descripcion_vacia():
    assert not menciona("", "AI")
    assert not menciona(None, "AI")
