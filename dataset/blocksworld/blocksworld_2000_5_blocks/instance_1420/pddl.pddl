

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c e)
(on d c)
(on e b)
(clear a)
)
(:goal
(and
(on a d)
(on b e)
(on d b)
(on e c))
)
)


