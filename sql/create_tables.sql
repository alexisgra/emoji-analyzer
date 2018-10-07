
-- Store scripts ending status.
CREATE TABLE ending_status(
    id SERIAL NOT NULL,
    label VARCHAR(10) NOT NULL COMMENT 'label of the script ending status',
    PRIMARY KEY(id)
);
-- Store the history of script runs.
CREATE TABLE script_runs (
    id SERIAL NOT NULL,
    dateBegin DATETIME NOT NULL,
    dateEnd DATETIME NOT NULL,
    ending_status BIGINT UNSIGNED NOT NULL COMMENT 'script ending status',
    PRIMARY KEY(id),
    FOREIGN KEY(ending_status) REFERENCES ending_status(id)
);
-- Store the most used emoji for a trend
CREATE TABLE twitt_france_trends(
    fk_script_run BIGINT UNSIGNED NOT NULL,
    trend VARCHAR(50) NOT NULL,
    emoji CHAR(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci COMMENT 'Most used emoji for the trend',
    FOREIGN KEY(fk_script_run) REFERENCES script_runs(id)
);