

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(on c e)
(on d c)
(ontable e)
(clear a)
(clear d)
)
(:goal
(and
(on b a)
(on c d)
(on d e)
(on e b))
)
)


