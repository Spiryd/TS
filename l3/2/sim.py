from typing import List
from random import random, randint
from time import sleep

JAMMING_SIGNAL = float('inf')
COLLISION_SIGNAL = float('-inf')


class Packet(object):
    """Represents a packet with value, time to live (ttl), and bleeding indicator."""

    def __init__(self, value=5, ttl=3):
        """Initialize a Packet object with the given value and time to live."""
        self._value = value
        self._ttl = ttl
        self._bleeding = False

    @property
    def value(self):
        """Get the value of the packet."""
        return self._value

    @value.setter
    def value(self, new_value):
        """Set the value of the packet."""
        self._value = new_value

    @property
    def ttl(self):
        """Get the time to live (ttl) of the packet."""
        return self._ttl

    @ttl.setter
    def ttl(self, new_ttl):
        """Set the time to live (ttl) of the packet."""
        self._ttl = new_ttl

    @property
    def bleeding(self):
        """Indicates whether the packet has lost some of its ttl or not."""
        return self._bleeding

    def decrease_ttl(self):
        """Decrease the time to live (ttl) of the packet by 1 and set the bleeding indicator."""
        self._ttl -= 1
        self._bleeding = True

    def __add__(self, foreign):
        """Override the '+' operator to merge two packets with sum of their values and ttl."""
        return Packet(value=self.value + foreign.value, ttl=self.ttl)


class Device(object):
    """Represents a device connected to the Ethernet cable."""

    def __init__(self, ethernet_cable_pos):
        """Initialize a Device object with the given Ethernet cable position."""
        self._ethernet_cable_pos = ethernet_cable_pos
        self._exp_backoff_iterator = 0
        self._until_next_packet = 0
        self._currently_transmitted_value = 0
        self._jamming_mode = False
        self._exp_backoff = False

    @property
    def ethernet_cable_pos(self):
        """Get the position of the device on the Ethernet cable."""
        return self._ethernet_cable_pos

    @property
    def exp_backoff_iterator(self):
        """Get the exponential backoff iterator value."""
        return self._exp_backoff_iterator

    @exp_backoff_iterator.setter
    def exp_backoff_iterator(self, new_val):
        """Set the exponential backoff iterator value."""
        self._exp_backoff_iterator = new_val

    @property
    def is_ready(self):
        """Check if the device is ready to send a packet."""
        if self.until_next_packet == 0 and self.currently_transmitted_value == 0 and not self.jamming_mode:
            return True
        else:
            return False

    def perform_exponential_backoff(self, packet_length):
        """Perform exponential backoff by setting 'until_next_packet' with a random value based on 'exp_backoff_iterator'."""
        k = 10 if self._exp_backoff_iterator > 10 else self._exp_backoff_iterator
        self._until_next_packet = randint(0, 2 ** k) * packet_length
        self._exp_backoff = True

    @property
    def currently_transmitted_value(self):
        """Get the value of the packet currently being transmitted by the device."""
        return self._currently_transmitted_value

    @currently_transmitted_value.setter
    def currently_transmitted_value(self, new_val):
        """Set the value of the packet currently being transmitted by the device."""
        self._currently_transmitted_value = new_val

    @property
    def jamming_mode(self):
        """Check if the device is in jamming mode."""
        return self._jamming_mode

    @jamming_mode.setter
    def jamming_mode(self, new_val):
        """Set the jamming mode state of the device."""
        self._jamming_mode = new_val

    @property
    def until_next_packet(self):
        """Get the remaining time until the device can send the next packet."""
        return self._until_next_packet

    @until_next_packet.setter
    def until_next_packet(self, new_val):
        """Set the remaining time until the device can send the next packet."""
        self._until_next_packet = new_val

    @property
    def exp_backoff(self):
        """Check if the device is in exponential backoff mode."""
        return self._exp_backoff

    def reset_exp_backoff(self):
        """Reset the exponential backoff mode and iterator."""
        self._exp_backoff = False
        self._exp_backoff_iterator = 0


def propagate(ethernet_cable: List[Packet]) -> bool:
    """Propagate packets further along the ethernet cable.

    Args:
        ethernet_cable: List of Packet objects representing the current state of the ethernet cable.

    Returns:
        bool: True if there are packets remaining on the ethernet cable, False otherwise.
    """

    i = 0
    while i < len(ethernet_cable):

        packet = ethernet_cable[i]

        if packet is not None:

            if packet.ttl < 2:
                # Kill the packet that has bled out
                ethernet_cable[i] = None

            if not packet.bleeding:

                if i > 0:
                    if ethernet_cable[i-1] is None:
                        ethernet_cable[i-1] = Packet(packet.value, ttl=packet.ttl)
                    elif ethernet_cable[i-1].value != packet.value:
                        ethernet_cable[i-1] = packet + ethernet_cable[i-1]

                if i < len(ethernet_cable) - 1:
                    if ethernet_cable[i+1] is None:
                        ethernet_cable[i+1] = Packet(packet.value, ttl=packet.ttl)
                        i += 1
                    elif ethernet_cable[i+1].value != packet.value:
                        ethernet_cable[i+1] = packet + ethernet_cable[i+1]
                        i += 1

            packet.decrease_ttl()

        i += 1

    return ethernet_cable


def can_send_packet(ethernet_cable: List[Packet], index: int) -> bool:
    """Check if a device can send a packet based on the current state of the ethernet cable.

    Args:
        ethernet_cable: List of Packet objects representing the current state of the ethernet cable.
        index: Index of the device on the ethernet cable.

    Returns:
        bool: True if the device can send a packet, False otherwise.
    """
    if ethernet_cable[index] is None :
        return True
    return False


def print_ethernet_cable(ethernet_cable):
    """Print the current state of the ethernet cable."""
    for el in map(lambda x: str('#' if x.value == JAMMING_SIGNAL else (x.value if x.value in [1, 2] else '!')) if x is not None else ' ', ethernet_cable):
        print(el, end=' ')
    print()
    
def simulate_csma_cd() -> None:
    """Simulate the CSMA/CD protocol.

    Args:
        ethernet_cable: List of Packet objects representing the initial state of the ethernet cable.
        devices: List of Device objects representing the devices connected to the ethernet cable.
        transmission_delay: Time delay between each step of the simulation.
    """
    # packets propagating down a virtual ethernet cable
    ethernet_cable = [None for _ in range(80)]
    # initialize the devices
    devices = [
        Device(20),
        Device(60)
    ]
    # how many iterations will pass
    simulation_duration = 2000
    # probability of a device to emit some data
    probability = 0.4
    # packet length
    packet_length = 2*len(ethernet_cable)

    #ethernet_cable[20] = Packet(value=1, ttl=packet_length)
    #ethernet_cable[60] = Packet(value=2, ttl=packet_length)
    devices[0].currently_transmitted_value = 1
    devices[1].currently_transmitted_value = 2

    data = 10
    for _ in range(1, simulation_duration+1):

        for device in devices:

            if device.exp_backoff_iterator > 15:
                # abort
                device.currently_transmitted_value = 0
                device.reset_exp_backoff()

            t = ethernet_cable[device.ethernet_cable_pos]

            if can_send_packet(ethernet_cable, device.ethernet_cable_pos):

                if device.until_next_packet == 0 and device.currently_transmitted_value != 0:
                    ethernet_cable[device.ethernet_cable_pos] = Packet(value=device.currently_transmitted_value,
                                                                       ttl=packet_length)
                else:
                    device.until_next_packet -= 1

            if t is not None and device.currently_transmitted_value != 0:
                # something is happening around the entrance of the device
                if t.value == device.currently_transmitted_value and t.ttl == 1:
                    # the packet has finished transferring
                    device.currently_transmitted_value = 0
                    # reset the exponential backoff if there was any
                    device.reset_exp_backoff()

                elif t.value not in [JAMMING_SIGNAL, device.currently_transmitted_value] and device.until_next_packet < 1:
                    # something is wrong and the jamming signal hasn't been transmitted yet
                    ethernet_cable[device.ethernet_cable_pos] = Packet(value=JAMMING_SIGNAL,
                                                                       ttl=packet_length)
                    device.exp_backoff_iterator += 1
                    device.perform_exponential_backoff(packet_length)

                if t.value == JAMMING_SIGNAL and device.until_next_packet == 0:
                    device.perform_exponential_backoff(packet_length)

        propagate(ethernet_cable)
        #sleep(0.008)
        print_ethernet_cable(ethernet_cable)

if __name__ == '__main__':
    simulate_csma_cd()
 