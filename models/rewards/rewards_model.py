from enum import Enum


class RewardStatus(str, Enum):
    TRANSFERRING = "transferring"
    CALCULATING = "calculating"
    TRANSFER_FAILED = "transfer_failed"
    CREATED = "created"
    TRANSFER_SUCCEEDED = "transfer_succeeded"
    FAILED = 'failed'


class ClaimRewardErrorMessages(str, Enum):
    ALREADY_IN_PROGRESS = "Another claim in progress"
    AMOUNT_TOO_SMALL = "Amount too small"
    ZERO_AMOUNT = "Reward amount is 0"
    EXCEEDS_DAILY_LIMIT = "Max daily claim limit reached"
    REWARD_CLAIMED = "Reward already claimed"
