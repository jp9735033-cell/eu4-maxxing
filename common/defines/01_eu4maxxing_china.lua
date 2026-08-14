-- eu4-maxxing: a divided China should be hard to hold together.
-- Vanilla ships this at 0.0, a leftover from pre-1.29 behaviour where
-- independent Chinese neighbours drained the Emperor's mandate.
-- Making it negative means every independent Chinese state bleeds the
-- Emperor of China, so reunification is contested rather than inevitable.
-- Delete this file to restore vanilla behaviour, or tune the number.

NDefines.NDiplomacy.CELESTIAL_EMPIRE_MANDATE_PER_HUNDRED_NONTRIBUTARY_DEV = -0.10
