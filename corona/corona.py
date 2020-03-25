#!/usr/bin/python3
import argparse
from argparse import ArgumentParser

from data import download_if_not_updated


DATA = download_if_not_updated()

def print_state_data(state_data: dict, rank: int) -> None:
        print(f""" State: {state_data['state']}, State rank: {rank}. Active: {state_data['active']} Confirmed: {state_data['confirmed']} Deaths: {state_data['deaths']} Recovered: {state_data['recovered']}""")

def get_state_info(state: str):
    if state is None or not isinstance(state, str):
        return

    state = state.lower()

    statewise = DATA["statewise"]
    state_data = None
    for rank, st in enumerate(statewise):
        # get the state data
        if state == st["state"].lower():
            state_data = st
            break
    else:
        # incorrect state
        print(f"State: {state} not found...")
        return

    print_state_data(state_data, rank=rank)

def get_rank_info(rank: int) -> None:
    if rank is None or not isinstance(rank, int):
        return

    statewise = DATA["statewise"]
    statewise.sort(key=lambda x: int(x['active']), reverse=True)
    if rank == -1:
        for r in range(len(statewise)):
            print_state_data(statewise[r], rank=r)
        return
    if rank < 0 or rank >= len(statewise):
        print(f"Rank should be between 0 and {len(statewise)}")
        return

    # data already sorted according to cases
    print_state_data(statewise[rank], rank=rank)


def main(args: argparse.Namespace) -> None:
    if not args.state and not args.rank:
        get_rank_info(-1)
    get_state_info(args.state)
    get_rank_info(args.rank)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("--rank", type=int, help="Rank of state in terms of cases")
    parser.add_argument("--state", type=str, help="Name of the state (Total for all states combined)")

    args = parser.parse_args()

    main(args)

