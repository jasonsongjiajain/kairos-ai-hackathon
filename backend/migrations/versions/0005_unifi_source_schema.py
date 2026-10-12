"""Add the lossless UniFi source schema alongside the application schema."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0005_unifi_source_schema"
down_revision = "0004_field_operations_facts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS unifi")

    op.create_table(
        "customers",
        sa.Column("login_id", sa.Text(), nullable=False),
        sa.Column("account_no", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("contact_no", sa.Text()),
        sa.Column("email_address", sa.Text()),
        sa.Column("address", sa.Text()),
        sa.Column("contract_term", sa.Integer()),
        sa.Column("commitment_start", sa.DateTime()),
        sa.Column("commitment_end", sa.DateTime()),
        sa.PrimaryKeyConstraint("login_id", name="customers_pkey"),
        schema="unifi",
    )
    op.create_table(
        "customer_summaries",
        sa.Column("login_id", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text()),
        sa.Column("model", sa.Text()),
        sa.Column("generated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("login_id", name="customer_summaries_pkey"),
        sa.ForeignKeyConstraint(
            ["login_id"], ["unifi.customers.login_id"],
            name="customer_summaries_login_id_fkey", ondelete="CASCADE",
        ),
        schema="unifi",
    )
    op.create_table(
        "devices",
        sa.Column("mac_address", sa.Text(), nullable=False),
        sa.Column("login_id", sa.Text(), nullable=False),
        sa.Column("friendly_name", sa.Text()),
        sa.Column("manufacturer", sa.Text()),
        sa.Column("brand", sa.Text()),
        sa.Column("device_type", sa.Text()),
        sa.Column("cloud_device_type", sa.Text()),
        sa.Column("link_type", sa.Text()),
        sa.Column("ip_address", postgresql.INET()),
        sa.Column("ssid_2_4ghz", sa.Text()),
        sa.Column("ssid_5ghz", sa.Text()),
        sa.Column("channel_2_4ghz", sa.Integer()),
        sa.Column("channel_5ghz", sa.Integer()),
        sa.Column("antenna_2_4ghz", sa.Text()),
        sa.Column("antenna_5ghz", sa.Text()),
        sa.Column("protocol_2_4ghz", sa.Text()),
        sa.Column("protocol_5ghz", sa.Text()),
        sa.Column("rssi", sa.Integer()),
        sa.Column("rx_rate", sa.Integer()),
        sa.Column("tx_rate", sa.Integer()),
        sa.Column("last_seen", sa.DateTime()),
        sa.Column("parent_mac", sa.Text()),
        sa.Column("platform", sa.Text()),
        sa.Column("bandwidth_2_4ghz", sa.Text()),
        sa.Column("bandwidth_5ghz", sa.Text()),
        sa.PrimaryKeyConstraint("mac_address", name="devices_pkey"),
        sa.ForeignKeyConstraint(
            ["login_id"], ["unifi.customers.login_id"],
            name="devices_login_id_fkey", ondelete="CASCADE",
        ),
        schema="unifi",
    )
    op.create_table(
        "routers",
        sa.Column("serial_number", sa.Text(), nullable=False),
        sa.Column("login_id", sa.Text(), nullable=False),
        sa.Column("manufacturer", sa.Text()),
        sa.Column("model", sa.Text()),
        sa.Column("cpu_usage_pct", sa.Integer()),
        sa.Column("cpu_temperature_c", sa.Integer()),
        sa.Column("memory_usage_pct", sa.Integer()),
        sa.Column("monthly_usage_gb", sa.Numeric(9, 1)),
        sa.Column("rx_power_dbm", sa.Numeric(5, 1)),
        sa.PrimaryKeyConstraint("serial_number", name="routers_pkey"),
        sa.ForeignKeyConstraint(
            ["login_id"], ["unifi.customers.login_id"],
            name="routers_login_id_fkey", ondelete="CASCADE",
        ),
        schema="unifi",
    )
    op.create_index("idx_devices_login_id", "devices", ["login_id"], schema="unifi")
    op.create_index("idx_routers_login_id", "routers", ["login_id"], schema="unifi")


def downgrade() -> None:
    op.execute("DROP SCHEMA IF EXISTS unifi CASCADE")
