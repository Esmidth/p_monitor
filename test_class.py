class Perf_Metric:
    nodeNum:int
    sec:int
    align_frame:int
    sent_frame:int
    forward_packets:int
    consume_packets:int
    missing_packets:int
    drop_frames:int
    missing_frames:int
    consumer_speed:int
    recv_speed:int
    queue1_size:int
    queue2_size:int
    queue3_size:int


perf_metrics = Perf_Metric()
perf_metrics.align_frame = 1

print(perf_metrics.align_frame)


