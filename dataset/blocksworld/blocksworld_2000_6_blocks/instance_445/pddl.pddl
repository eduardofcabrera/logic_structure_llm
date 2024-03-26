

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b a)
(ontable c)
(on d e)
(ontable e)
(clear b)
(clear c)
)
(:goal
(and
(on a b)
(on b d)
(on d e)
(on e c))
)
)


