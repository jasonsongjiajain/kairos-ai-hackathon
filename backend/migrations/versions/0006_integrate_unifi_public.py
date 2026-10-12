"""Expose the detailed UniFi source data through the public application schema."""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "0006_integrate_unifi_public"
down_revision = "0005_unifi_source_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    customer_columns = [
        sa.Column("account_no", sa.Text()),
        sa.Column("contact_no", sa.Text()),
        sa.Column("email_address", sa.Text()),
        sa.Column("contract_term", sa.Integer()),
        sa.Column("commitment_start", sa.DateTime()),
        sa.Column("commitment_end", sa.DateTime()),
    ]
    for column in customer_columns:
        op.add_column("customers", column)

    device_columns = [
        sa.Column("mac_address", sa.Text()),
        sa.Column("login_id", sa.Text()),
        sa.Column("friendly_name", sa.Text()),
        sa.Column("manufacturer", sa.Text()),
        sa.Column("brand", sa.Text()),
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
    ]
    for column in device_columns:
        op.add_column("network_devices", column)

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
        schema="public",
    )
    op.create_index("idx_routers_login_id", "routers", ["login_id"], schema="public")

    op.create_table(
        "customer_summaries",
        sa.Column("login_id", sa.Text(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text()),
        sa.Column("model", sa.Text()),
        sa.Column("generated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("login_id", name="customer_summaries_pkey"),
        schema="public",
    )

    op.execute("""
        INSERT INTO public.customers
            (id, customer_ref, name, address, is_demo, account_no, contact_no,
             email_address, contract_term, commitment_start, commitment_end)
        SELECT md5('unifi:customer:' || login_id)::uuid, login_id, name,
               COALESCE(address, ''), false, account_no, contact_no,
               email_address, contract_term, commitment_start, commitment_end
        FROM unifi.customers
        ON CONFLICT (customer_ref) DO UPDATE SET
            name = EXCLUDED.name,
            address = EXCLUDED.address,
            account_no = EXCLUDED.account_no,
            contact_no = EXCLUDED.contact_no,
            email_address = EXCLUDED.email_address,
            contract_term = EXCLUDED.contract_term,
            commitment_start = EXCLUDED.commitment_start,
            commitment_end = EXCLUDED.commitment_end
    """)
    op.execute("""
        INSERT INTO public.network_devices
            (id, customer_id, device_ref, device_type, name, status, details,
             mac_address, login_id, friendly_name, manufacturer, brand,
             cloud_device_type, link_type, ip_address, ssid_2_4ghz, ssid_5ghz,
             channel_2_4ghz, channel_5ghz, antenna_2_4ghz, antenna_5ghz,
             protocol_2_4ghz, protocol_5ghz, rssi, rx_rate, tx_rate, last_seen,
             parent_mac, platform, bandwidth_2_4ghz, bandwidth_5ghz)
        SELECT md5('unifi:device:' || d.mac_address)::uuid,
               c.id, d.mac_address, COALESCE(d.device_type, 'unknown'),
               COALESCE(d.friendly_name, d.mac_address), 'unknown', '{}'::json,
               d.mac_address, d.login_id, d.friendly_name, d.manufacturer,
               d.brand, d.cloud_device_type, d.link_type, d.ip_address,
               d.ssid_2_4ghz, d.ssid_5ghz, d.channel_2_4ghz, d.channel_5ghz,
               d.antenna_2_4ghz, d.antenna_5ghz, d.protocol_2_4ghz,
               d.protocol_5ghz, d.rssi, d.rx_rate, d.tx_rate, d.last_seen,
               d.parent_mac, d.platform, d.bandwidth_2_4ghz, d.bandwidth_5ghz
        FROM unifi.devices d
        JOIN public.customers c ON c.customer_ref = d.login_id
        ON CONFLICT (device_ref) DO UPDATE SET
            customer_id = EXCLUDED.customer_id,
            device_type = EXCLUDED.device_type,
            name = EXCLUDED.name,
            mac_address = EXCLUDED.mac_address,
            login_id = EXCLUDED.login_id,
            friendly_name = EXCLUDED.friendly_name,
            manufacturer = EXCLUDED.manufacturer,
            brand = EXCLUDED.brand,
            cloud_device_type = EXCLUDED.cloud_device_type,
            link_type = EXCLUDED.link_type,
            ip_address = EXCLUDED.ip_address,
            ssid_2_4ghz = EXCLUDED.ssid_2_4ghz,
            ssid_5ghz = EXCLUDED.ssid_5ghz,
            channel_2_4ghz = EXCLUDED.channel_2_4ghz,
            channel_5ghz = EXCLUDED.channel_5ghz,
            antenna_2_4ghz = EXCLUDED.antenna_2_4ghz,
            antenna_5ghz = EXCLUDED.antenna_5ghz,
            protocol_2_4ghz = EXCLUDED.protocol_2_4ghz,
            protocol_5ghz = EXCLUDED.protocol_5ghz,
            rssi = EXCLUDED.rssi,
            rx_rate = EXCLUDED.rx_rate,
            tx_rate = EXCLUDED.tx_rate,
            last_seen = EXCLUDED.last_seen,
            parent_mac = EXCLUDED.parent_mac,
            platform = EXCLUDED.platform,
            bandwidth_2_4ghz = EXCLUDED.bandwidth_2_4ghz,
            bandwidth_5ghz = EXCLUDED.bandwidth_5ghz
    """)
    op.execute("""
        INSERT INTO public.routers
            (serial_number, login_id, manufacturer, model, cpu_usage_pct,
             cpu_temperature_c, memory_usage_pct, monthly_usage_gb, rx_power_dbm)
        SELECT serial_number, login_id, manufacturer, model, cpu_usage_pct,
               cpu_temperature_c, memory_usage_pct, monthly_usage_gb, rx_power_dbm
        FROM unifi.routers
        ON CONFLICT (serial_number) DO UPDATE SET
            login_id = EXCLUDED.login_id,
            manufacturer = EXCLUDED.manufacturer,
            model = EXCLUDED.model,
            cpu_usage_pct = EXCLUDED.cpu_usage_pct,
            cpu_temperature_c = EXCLUDED.cpu_temperature_c,
            memory_usage_pct = EXCLUDED.memory_usage_pct,
            monthly_usage_gb = EXCLUDED.monthly_usage_gb,
            rx_power_dbm = EXCLUDED.rx_power_dbm
    """)
    op.execute("""
        INSERT INTO public.customer_summaries
            (login_id, summary, recommendation, model, generated_at)
        SELECT login_id, summary, recommendation, model, generated_at
        FROM unifi.customer_summaries
        ON CONFLICT (login_id) DO UPDATE SET
            summary = EXCLUDED.summary,
            recommendation = EXCLUDED.recommendation,
            model = EXCLUDED.model,
            generated_at = EXCLUDED.generated_at
    """)


def downgrade() -> None:
    op.drop_table("customer_summaries", schema="public")
    op.drop_index("idx_routers_login_id", table_name="routers", schema="public")
    op.drop_table("routers", schema="public")
    for name in reversed([
        "bandwidth_5ghz", "bandwidth_2_4ghz", "platform", "parent_mac",
        "last_seen", "tx_rate", "rx_rate", "rssi", "protocol_5ghz",
        "protocol_2_4ghz", "antenna_5ghz", "antenna_2_4ghz", "channel_5ghz",
        "channel_2_4ghz", "ssid_5ghz", "ssid_2_4ghz", "ip_address",
        "link_type", "cloud_device_type", "brand", "manufacturer",
        "friendly_name", "login_id", "mac_address",
    ]):
        op.drop_column("network_devices", name)
    for name in reversed([
        "commitment_end", "commitment_start", "contract_term", "email_address",
        "contact_no", "account_no",
    ]):
        op.drop_column("customers", name)
