import argparse
import socket
import statistics
import time
from datetime import datetime


def measure_tcp_latency(target_ip: str, target_port: int, timeout: float = 1.0) -> float | None:
    """
    Misst die Dauer eines TCP-Handshakes (SYN -> SYN-ACK -> ACK) in Mikrosekunden.
    Gibt None zurück, wenn die Verbindung fehlschlägt oder in den Timeout läuft.
    """
    start_time = time.perf_counter_ns()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((target_ip, target_port))
        end_time = time.perf_counter_ns()
        sock.close()
        # Nanosekunden in Mikrosekunden (µs) umrechnen
        return (end_time - start_time) / 1_000.0
    except (socket.timeout, socket.error, ConnectionRefusedError, OSError):
        return None


def run_benchmark(target_ip: str, target_port: int, count: int, interval: float, timeout: float):
    print(f"--- Layer-4 TCP Benchmark gegen {target_ip}:{target_port} ---")
    print(f"Messungen: {count} | Intervall: {interval}s | Timeout: {timeout}s\n")

    latencies_us = []
    failed_attempts = 0

    for i in range(1, count + 1):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        latency_us = measure_tcp_latency(target_ip, target_port, timeout)

        if latency_us is not None:
            latencies_us.append(latency_us)
            print(f"[{timestamp}] #{i:04d}: {latency_us:8.2f} µs ({latency_us / 1000.0:.4f} ms)")
        else:
            failed_attempts += 1
            print(f"[{timestamp}] #{i:04d}: FEHLGESCHLAGEN / TIMEOUT")

        if i < count and interval > 0:
            time.sleep(interval)

    # Statistische Auswertung
    print("\n" + "=" * 60)
    print(f"STATISTISCHE AUSWERTUNG ({target_ip}:{target_port})")
    print("=" * 60)

    total_requests = count
    successful_requests = len(latencies_us)
    loss_rate = (failed_attempts / total_requests) * 100

    print(f"Gesendet:        {total_requests}")
    print(f"Erfolgreich:     {successful_requests}")
    print(f"Fehlgeschlagen:  {failed_attempts} ({loss_rate:.2f}% Paketverlust)")

    if successful_requests > 0:
        sorted_lat = sorted(latencies_us)
        min_val = min(sorted_lat)
        max_val = max(sorted_lat)
        mean_val = statistics.mean(sorted_lat)
        median_val = statistics.median(sorted_lat)
        stdev_val = statistics.stdev(sorted_lat) if len(sorted_lat) > 1 else 0.0

        p95_index = max(0, int(0.95 * len(sorted_lat)) - 1)
        p99_index = max(0, int(0.99 * len(sorted_lat)) - 1)
        p95_val = sorted_lat[p95_index]
        p99_val = sorted_lat[p99_index]

        print("-" * 60)
        print(f"Minimum:         {min_val:8.2f} µs ({min_val / 1000.0:.4f} ms)")
        print(f"Maximum:         {max_val:8.2f} µs ({max_val / 1000.0:.4f} ms)")
        print(f"Mittelwert:      {mean_val:8.2f} µs ({mean_val / 1000.0:.4f} ms)")
        print(f"Median:          {median_val:8.2f} µs ({median_val / 1000.0:.4f} ms)")
        print(f"Std.-Abweichung: {stdev_val:8.2f} µs ({stdev_val / 1000.0:.4f} ms)")
        print(f"95. Perzentil:   {p95_val:8.2f} µs ({p95_val / 1000.0:.4f} ms)")
        print(f"99. Perzentil:   {p99_val:8.2f} µs ({p99_val / 1000.0:.4f} ms)")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="High-Precision Layer-4 TCP Latency Benchmark")
    parser.add_argument("host", help="Ziel-IP-Adresse")
    parser.add_argument("-p", "--port", type=int, default=5432, help="Ziel-Port (Standard: 5432)")
    parser.add_argument("-c", "--count", type=int, default=100, help="Anzahl Messungen (Standard: 100)")
    parser.add_argument("-i", "--interval", type=float, default=0.01, help="Pause zwischen Paketen in Sek. (Standard: 0.01)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, help="Connect Timeout in Sek. (Standard: 1.0)")

    args = parser.parse_args()
    run_benchmark(args.host, args.port, args.count, args.interval, args.timeout)
