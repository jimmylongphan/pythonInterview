import uuid

class DbConnection:
    """
    You SHOULD NOT NEED TO MODIFY this class.
     
    This is a mock database connection that simply prints the query, and
    represents a connection to a database, e.g. MySQL, Postgres, MongoDB, etc.
    """
    def __init__(self):
        self.id = str(uuid.uuid4())[0:8]
        print("Created DbConnection with ID " + self.id)

    def query(self, q: str) -> str:
        print(f"DbConnection {self.id} ran query \"{q}\"")
        return "my query result"


class ConnectionPool:
    """
    A ConnectionPool is responsible for making available PooledConnections to clients for querying.
 
    It manages the lifecycle of a pool of underlying DbConnections and creates them only as needed (lazily),
    up to a maximum number of connections.
 
    When a PooledConnection is closed, the underlying DbConnection is returned to this pool for later reuse.

    NOTES:
    - DBConnection is created up to a fixed size. These are reusable between PooledConnections
    - PooledConnections are only used per client. They can be used until they call closed
    - After closing, the PooledConnections still exist, but the DBConnection is returned and re-used
    
    """
    

    def __init__(self, max_num_connections: int):
        """
        Instantiate a new ConnectionPool.

        :param max_num_connections: positive integer
        :raises ValueError: with message "maxNumConnections must be positive" if max_num_connections is not positive
        """
        self._max_num_connections = max_num_connections
        self.available_db_connections = []
        self.db_connections_created = 0
        
        # TODO: Implement this method
        if max_num_connections <= 0:
            raise ValueError("maxNumConnections must be positive")

    def get_connection(self):
        """
        Return a PooledConnection wrapping a DbConnection from the pool.

        :return: a PooledConnection, or None if no more connections are available.
        """
        # check if there is availbility for a PooledConnection
        if len(self.available_db_connections) > 0:
            dbc = self.available_db_connections.pop()
            pc = PooledConnection(self, dbc) 
            return pc

        # there are no avaiable PooledConnections, but have not reach the max, create a new one 
        if self.db_connections_created < self._max_num_connections:
            dbc = DbConnection()
            pc = PooledConnection(self, dbc)
            self.db_connections_created += 1
            return pc
        
        # no available and max has been reached     
        return None
        
    def free_connection(self, dbc: DbConnection):
        """
        save the reusable db connection
        """
        self.available_db_connections.append(dbc)


class PooledConnection:
    """
    A PooledConnection is an abstraction over a regular DbConnection to faciliate DbConnection reuse.
 
    It wraps an underlying DbConnection and is returned by a ConnectionPool.
    """

    def __init__(self, parent: ConnectionPool, db_connection: DbConnection):
        self._parent = parent
        self._db_connection = db_connection
        self.closed = False


    def query(self, q: str) -> str:
        """
        Execute provided query `q` on the wrapped DbConnection.

        :param q: query string
        :raises Exception: if PooledConnection is closed
        :return: query result
        """
        if self.closed:
            raise Exception("PooledConnection is closed")
        
        return self._db_connection.query(q)
        

    def close(self) -> None:
        """
        Close the connection.
     
        This method frees the DbConnection to the ConnectionPool for later reuse.
     
        This PooledConnection should not be reused after they are closed. 
        
        Repeated calls to close() are idempotent.
        """
        if self.closed is True:
            return

        self.closed = True
        self._parent.free_connection(self._db_connection)


# ---------------------------------------------
# Test Helper

def assert_raises(fn, includes=None, assertion_message=None) -> None:
    """
    Assert that the provided function `fn` raises an exception.
    :param fn: Function that should raise an exception
    :param includes: Check that the exception message includes this text
    :param assertion_message: Message to include in the assertion error
    """
    try:
        fn()
    except Exception as ex:
        if includes:
            msg = repr(ex)
            assert includes in msg, \
                f"Exception message '{msg}' does not contain expected text '{includes}'"
        return
    assert False, f"Expected function to raise error {assertion_message or ''}"

# ---------------------------------------------
# Tests

def test_basic_operations():
    print("Test basic operations")
    pool = ConnectionPool(1)
    conn1 = pool.get_connection()
    assert conn1 is not None, "Should have returned a connection"
    conn1.query("my fun query")
    conn1.close()

    # reusing underlying db connection
    conn2 = pool.get_connection()
    conn2.query("another fun query")
    conn2.close()


def test_pool_cannot_be_created_with_non_positive_max_num_connections():
    print("Test pool cannot be created with non-positive maxNumConnections")
    assert_raises(lambda: ConnectionPool(0), 'maxNumConnections must be positive',
                  'Should have errored when creating pool with 0 maxNumConnections')

    assert_raises(lambda: ConnectionPool(-1), 'maxNumConnections must be positive',
                  'Should have errored when creating pool with -1 maxNumConnections')


def test_connections_are_lazily_created():
    print("Test connections are lazily created")

    pool = ConnectionPool(1)
    conn1 = pool.get_connection()
    conn1.close()

    # reusing underlying db connection
    conn2 = pool.get_connection()
    assert conn1._db_connection.id == conn2._db_connection.id


def test_more_than_max_num_connections_cannot_be_created():
    print("Test more than maxNumConnections cannot be created")

    pool = ConnectionPool(1)
    _ = pool.get_connection()

    # reusing underlying db connection
    conn2 = pool.get_connection()
    assert conn2 is None


def test_connections_are_reused_after_closing():
    print("Test connections are reused after closing")

    pool = ConnectionPool(1)
    conn1 = pool.get_connection()
    conn1.query("my fun query")
    conn1.close()

    # reusing underlying db connection
    conn2 = pool.get_connection()
    conn2.query("another fun query")
    conn2.close()

    assert conn1._db_connection.id == conn2._db_connection.id


def test_connection_close_is_idempotent():
    print("Test connection close is idempotent")
    pool = ConnectionPool(1)
    conn1 = pool.get_connection()
    conn1.close()
    conn1.close()
    conn1.close()
    assert len(pool.available_db_connections) == 1


def test_connection_cannot_be_queried_after_close():
    print("Test connection cannot be queried after close")

    pool = ConnectionPool(1)
    conn1 = pool.get_connection()
    conn1.query("my fun query before close")
    conn1.close()

    assert_raises(lambda: conn1.query("my fun query after close") , includes='PooledConnection is closed')

def main():
    test_basic_operations()
    test_pool_cannot_be_created_with_non_positive_max_num_connections()
    test_connections_are_lazily_created()
    test_more_than_max_num_connections_cannot_be_created()
    test_connections_are_reused_after_closing()
    test_connection_close_is_idempotent()
    test_connection_cannot_be_queried_after_close()


main()
