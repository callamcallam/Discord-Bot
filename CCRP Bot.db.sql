BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Welcome System" (
	"welcome_system"	INTEGER NOT NULL,
	"welcome_channel"	INTEGER,
	"welcome_message"	TEXT,
	"welcome_role"	INTEGER,
	"welcome_image"	TEXT,
	PRIMARY KEY("welcome_system")
);
CREATE TABLE IF NOT EXISTS "Leave System" (
	"leave_system"	INTEGER NOT NULL,
	"leave_channel"	INTEGER,
	"leave_message"	TEXT,
	"leave_image"	TEXT,
	PRIMARY KEY("leave_system")
);
CREATE TABLE IF NOT EXISTS "Discord Bans" (
	"user-id"	INTEGER NOT NULL UNIQUE,
	"reason"	TEXT,
	"date"	TEXT,
	"banned-by"	INTEGER NOT NULL,
	PRIMARY KEY("user-id")
);
CREATE TABLE IF NOT EXISTS "Discord Kicks" (
	"user-id"	INTEGER NOT NULL,
	"reason"	TEXT,
	"date"	TEXT,
	"kicked-by"	INTEGER NOT NULL,
	PRIMARY KEY("user-id")
);
CREATE TABLE IF NOT EXISTS "Discord Mutes" (
	"user-id"	INTEGER NOT NULL,
	"reason"	TEXT,
	"date"	TEXT,
	"muted-by"	INTEGER NOT NULL,
	PRIMARY KEY("user-id")
);
CREATE TABLE IF NOT EXISTS "FiveM Bans" (
	"Discord ID"	INTEGER,
	"Steam Hex"	TEXT,
	"FiveM"	TEXT,
	"Evidence"	TEXT,
	"Reason"	TEXT,
	"Banned By"	TEXT,
	"Ban Duration"	TEXT,
	"Ban Date"	TEXT,
	"Banned User"	TEXT,
	PRIMARY KEY("Steam Hex","Discord ID","FiveM","Evidence","Reason","Banned By","Ban Duration","Ban Date","Banned User")
);
CREATE TABLE IF NOT EXISTS "FiveM Notes" (
	"Discord ID"	INTEGER,
	"Steam Hex"	TEXT,
	"FiveM"	TEXT,
	"Notes"	TEXT,
	"Note By"	TEXT,
	"Note Date"	TEXT,
	"Noted User"	TEXT,
	"Unique Key"	TEXT UNIQUE,
	PRIMARY KEY("FiveM","Discord ID","Unique Key")
);
CREATE TABLE IF NOT EXISTS "FiveM Warns" (
	"Discord ID"	INTEGER,
	"Steam Hex"	TEXT,
	"FiveM"	TEXT,
	"Evidence"	TEXT,
	"Reason"	TEXT,
	"Warned By"	TEXT,
	"Warn Date"	TEXT,
	"Warned User"	TEXT,
	PRIMARY KEY("Steam Hex","Discord ID","FiveM","Evidence","Reason","Warned By","Warn Date","Warned User")
);
CREATE TABLE IF NOT EXISTS "Config" (
	"token"	TEXT NOT NULL,
	"guild_id"	INTEGER,
	"command_prefix"	TEXT,
	"status"	TEXT,
	"status_type"	TEXT,
	"webhook_url"	TEXT,
	"Staff Team ID"	INTEGER,
	PRIMARY KEY("token")
);
CREATE TABLE IF NOT EXISTS "Ticket System" (
	"ticket_system"	INTEGER NOT NULL,
	"ticket_channel"	INTEGER,
	"support_role"	INTEGER,
	"support_category"	INTEGER,
	"support_welcome_message"	TEXT,
	"support_claim_message"	TEXT,
	"support_close_message"	TEXT,
	"donation_category"	INTEGER,
	"donation_welcome_message"	TEXT,
	"donation_claim_message"	TEXT,
	"donation_close_message"	TEXT,
	"ban_category"	INTEGER,
	"ban_welcome_message"	TEXT,
	"ban_claim_message"	TEXT,
	"ban_close_message"	TEXT,
	"transcripts"	iNTEGER NOT NULL,
	"general-support-transcript-channel"	INTEGER,
	"donation-transcript-channel"	INTEGER,
	"ban-transcript-channel"	INTEGER,
	PRIMARY KEY("ticket_system","transcripts")
);
CREATE TABLE IF NOT EXISTS "Open Tickets" (
	"uuid"	TEXT NOT NULL,
	"user-id"	INTEGER NOT NULL,
	"ticket-type"	TEXT NOT NULL,
	"channel_id"	INTEGER,
	"claimed-by"	INTEGER,
	"is-locked"	INTEGER,
	PRIMARY KEY("uuid")
);
COMMIT;
