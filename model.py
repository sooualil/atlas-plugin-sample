import os
from joblib import load
from typing import Any, Dict, List
from pandas import DataFrame

from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.tree import ExtraTreeClassifier


class Model:
    columns: List[str]
    columns_to_encode: List[str]
    columns_encoder: Dict[str, LabelEncoder]
    label_encoder: LabelEncoder
    # features_scaler: MinMaxScaler
    model: ExtraTreeClassifier

    def __init__(self, path):
        self.path = path
        self.model = self.p_load('model')
        self.columns = self.p_load('columns')
        # self.columns_to_encode = ['protocol',  'application_name', 'application_category_name', 'content_type']
        self.columns_to_encode = []
        self.columns_encoder = {
            col: self.p_load(col)
            for col in [
                'protocol', 'application_name', 'application_category_name',
                'content_type'
            ]
        }
        self.label_encoder = self.p_load('attack_encoder')
        self.columns_to_delete = ['udps.bidirectional_pkts', 'Attack']
        self.additional_columns = [
            'udps.num_pkts_up_to_128_bytes', 'udps.num_pkts_128_to_256_bytes',
            'udps.num_pkts_256_to_512_bytes',
            'udps.num_pkts_512_to_1024_bytes',
            'udps.num_pkts_1024_to_1514_bytes', 'udps.min_ttl', 'udps.max_ttl',
            'udps.min_ip_pkt_len', 'udps.max_ip_pkt_len', 'udps.src2dst_flags',
            'udps.dst2src_flags', 'udps.tcp_flags', 'udps.tcp_win_max_in',
            'udps.tcp_win_max_out', 'udps.icmp_type', 'udps.icmp_v4_type',
            'udps.dns_query_id', 'udps.dns_query_type', 'udps.dns_ttl_answer',
            'udps.ftp_command_ret_code', 'udps.retransmitted_in_packets',
            'udps.retransmitted_out_packets', 'udps.retransmitted_in_bytes',
            'udps.retransmitted_out_bytes', 'udps.src_to_dst_second_bytes',
            'udps.dst_to_src_second_bytes', 'udps.src_to_dst_avg_throughput',
            'udps.dst_to_src_avg_throughput', 'udps.src_to_dst_second_bytes2',
            'udps.dst_to_src_second_bytes2', 'udps.src_to_dst_avg_throughput2',
            'udps.dst_to_src_avg_throughput2'
        ]

    def p_load(self, name):
        return load(open(os.path.join(self.path, name + '.joblib'), 'rb'))

    def preprocess_df(self, test: Dict[str, List]):
        """
        This function preprocess the raw data, performing columns selection, encoding and features scalung
        """
        df_test = DataFrame(test)
        # df_test = df_test.drop(columns=self.columns_to_delete, axis=1)

        df_test = df_test[df_test.columns & self.columns]
        for col in self.columns_to_encode:
            # df_test[col] = df_test[col].str.strip()
            df_test[col] = self.columns_encoder[col].transform(df_test[col])
        return df_test

    def predict(self, test):
        X_test = self.preprocess_df(test)
        predictions = self.model.predict(X_test.values)
        predicted_labels = self.label_encoder.inverse_transform(predictions)
        return predictions, predicted_labels
