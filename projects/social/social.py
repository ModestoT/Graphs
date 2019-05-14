import random

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # Add users
        for i in range(numUsers):
            self.addUser(f"User {i + 1}")

        # Create friendships
        # avgFriendships = totalFriendships / numUsers
        # totalFriendships = avgFriendships * numUsers
        possibleFriendships = []
        for userID in self.users:
            for friendID in range(userID + 1, self.lastID + 1):
                possibleFriendships.append((userID, friendID))

        random.shuffle(possibleFriendships)

        for friendship_index in range(avgFriendships * numUsers // 2):
            friendship = possibleFriendships[friendship_index]
            self.addFriendship(friendship[0], friendship[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # Create an empty Queue
        q = []
        # Create an empty Visited set
        visited = {}  # Note that this is a dictionary, not a set
        # Add A PATH TO the starting user ID to the queue
        q.append( [userID] )
        # While the queue is not empty...
        while len(q) > 0:
            # Dequeue the first PATH
            path = q.pop(0)
            # Grab the last friend id of the path
            v = path[-1]
            # If it has not been visited...
            if v not in visited:
                # Mark it as visted and set the key as the friend id and the value as the path to that friend id
                visited[v] = path
                # Then enqueue PATHS TO each of its neighbors in the queue
                for neighbor in self.friendships[v]:
                    path_copy = path.copy()
                    path_copy.append(neighbor)
                    q.append(path_copy)
                    
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(10, 2)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)
