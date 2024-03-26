

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c d)
(on d b)
(ontable e)
(clear c)
(clear e)
)
(:goal
(and
(on a d)
(on c a)
(on e b))
)
)


